#!/usr/bin/env python3
# -*- coding: utf-8 -*
# sample_python aims to allow seamless integration with lua.
# see examples below

import os
import sys
import pdb  # use pdb.set_trace() for debugging
# or use code.interact(local=dict(globals(), **locals()))  for debugging.
import code
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image
from pprint import pprint


class Color:
    def __init__(self, R, G, B):
        self.color = np.array([R, G, B]).astype(np.float_)

    def gammaCorrect(self, gamma):
        inverseGamma = 1.0 / gamma
        self.color = np.power(self.color, inverseGamma)

    def toUINT8(self):
        return (np.clip(self.color, 0, 1) * 255).astype(np.uint8)

    def __add__(self, other):
        if other.__class__.__name__ == 'ndarray':
            return self.color + other
        else:
            return self.color + other.color

    def __str__(self):
        return "{0}".format(self.color)


class Light:
    def __init__(self, position, intensity):
        self.position = position
        self.intensity = intensity

    def __str__(self):
        ret = "position = {0}, intensity = {1}".format(
            self.position, self.intensity)
        return ret


class Surface:
    def __init__(self, type, shader):
        self.type = type
        self.shader = shader

    def __str__(self):
        ret = "type = {0}, shader = {1}".format(self.type, self.shader)
        return ret


class Sphere(Surface):
    def __init__(self, radius, center, type, shader):
        super().__init__(type, shader)
        self.radius = radius
        self.center = center

    def __str__(self):
        ret = "radius = {0}, center = {1}".format(self.radius, self.center)
        return ret


class Box(Surface):
    def __init__(self, mitPt, maxPt, type, shader):
        super().__init__(type, shader)
        self.mitPt = mitPt
        self.maxPt = maxPt

    def __str__(self):
        ret = "mitPt = {0}, maxPt = {1}".format(self.mitPt, self.maxPt)
        return ret


class Shader:
    def __init__(self, type, diffuse):
        self.type = type
        self.diffuse = diffuse

    def __str__(self):
        ret = "type = {0}".format(self.type)
        return ret


class ShaderPhong(Shader):
    def __init__(self, diffuse, specular, exponent, type):
        super().__init__(type, diffuse)
        self.specular = specular
        self.exponent = exponent

    def __str__(self):
        ret = "diffuse = {0}, specular = {1}, exponent = {2}".format(
            self.diffuse, self.specular, self.exponent)
        return ret


class ShaderLambertian(Shader):
    def __init__(self, diffuse, type):
        super().__init__(type, diffuse)

    def __str__(self):
        ret = "diffuse = {0}".format(self.diffuse)
        return ret


class View:
    def __init__(self, viewPoint, viewDir, viewUp, projNormal, viewWidth, viewHeight,
                 projDistance, intensity):
        self.viewPoint = viewPoint
        self.viewDir = viewDir
        self.viewUp = viewUp
        self.projNormal = projNormal
        self.viewWidth = viewWidth
        self.viewHeight = viewHeight
        self.projDistance = projDistance
        self.intensity = intensity


INF = sys.maxsize


def main():
    global img
    global BLACK
    global ambient
    amb = 0/255
    ambient = np.array([amb, amb, amb]).astype(np.float_)
    BLACK = np.array([0, 0, 0]).astype(np.float_)

    tree = ET.parse(sys.argv[1])
    root = tree.getroot()

    # set default values
    viewDir = np.array([0, 0, -1]).astype(np.float_)
    # you can safely assume this. (no examples will use shifted perspective camera)
    projNormal = -1*viewDir
    viewUp = np.array([0, 1, 0]).astype(np.float_)
    projDistance = 1.0
    viewWidth = 1.0
    viewHeight = 1.0
    # how bright the light is.
    intensity = np.array([1, 1, 1]).astype(np.float_)

    # set Camera view
    for c in root.findall('camera'):
        viewPoint = np.array(c.findtext('viewPoint').split()).astype(np.float_)
        viewDir = np.array(c.findtext('viewDir').split()).astype(np.float_)
        if (c.findtext('projNormal')):
            projNormal = np.array(c.findtext(
                'projNormal').split()).astype(np.float_)
        viewUp = np.array(c.findtext('viewUp').split()).astype(np.float_)
        if (c.findtext('projDistance')):
            projDistance = np.array(c.findtext(
                'projDistance').split()).astype(np.float_)
        viewWidth = np.array(c.findtext('viewWidth').split()).astype(np.float_)
        viewHeight = np.array(c.findtext(
            'viewHeight').split()).astype(np.float_)

    view = View(viewPoint, viewDir, viewUp, projNormal, viewWidth, viewHeight, projDistance, intensity)

    # Set Img Size
    imgSize = np.array(root.findtext('image').split()).astype(np.int_)

    # Shaders Dictionary
    # {'name' : shaderClass }
    shaders = dict()
    for c in root.findall('shader'):
        name = c.get('name')
        _type = c.get('type')
        if _type == 'Phong':
            diffuseColor_c = np.array(c.findtext(
                'diffuseColor').split()).astype(np.float_)
            specularColor = np.array(c.findtext(
                'specularColor').split()).astype(np.float_)
            exponent = np.array(c.findtext(
                'exponent').split()).astype(np.float_)
            shader = ShaderPhong(diffuse=diffuseColor_c, specular=specularColor, exponent=exponent, type=_type)
        else:
            diffuseColor_c = np.array(c.findtext(
                'diffuseColor').split()).astype(np.float_)
            shader = ShaderLambertian(diffuse=diffuseColor_c, type=_type)
        shaders[name] = shader

    # Surface List
    surfaces = list()
    for c in root.findall('surface'):
        shader = shaders[c[0].get('ref')]
        _type = c.get('type')
        if _type == 'Sphere':
            radius = np.array(c.findtext('radius').split()).astype(np.float_)
            center = np.array(c.findtext('center').split()).astype(np.float_)
            surface = Sphere(radius=radius, center=center,
                             type=_type, shader=shader)
        else:
            minPt = np.array(c.findtext('minPt').split()).astype(np.float_)
            maxPt = np.array(c.findtext('maxPt').split()).astype(np.float_)
            surface = Box(minPt=minPt, maxPt=maxPt, type=_type, shader=shader)
        surfaces.append(surface)

    # Light list
    lights = list()
    for c in root.findall('light'):
        position = np.array(c.findtext('position').split()).astype(np.float_)
        intensity = np.array(c.findtext('intensity').split()).astype(np.float_)
        light = Light(position=position, intensity=intensity)
        lights.append(light)

    # Create an empty image
    channels = 3
    img = np.zeros((imgSize[1], imgSize[0], channels), dtype=np.uint8)
    img[:, :] = 0

    img_tmp = mapPixelToImage(view, imgSize, surfaces, lights)
    for i in np.arange(imgSize[1]):
        for j in np.arange(imgSize[0]):
            img[i][j] = img_tmp[i][j]

    rawimg = Image.fromarray(img, 'RGB')
    rawimg.save(sys.argv[1]+'.png')
    # rawimg.save(sys.argv[1]+'.png')

# make vector as Unit vector


def makeUnitVector(vector):
    return vector / np.linalg.norm(vector)

# Calculate view direction of each pixels.


def mapPixelToImage(view, imgSize, surfaces, lights):
    view_point = view.viewPoint              # e
    dist_img_plane = view.projDistance       # d

    u_img_plane = np.cross(view.viewDir, view.viewUp)  # u
    v_img_plane = -np.cross(u_img_plane, view.viewDir)  # v
    w_img_plane = np.cross(u_img_plane, -v_img_plane)  # w                        # w

    u_unit = makeUnitVector(u_img_plane)
    v_unit = makeUnitVector(v_img_plane)
    w_unit = makeUnitVector(w_img_plane)

    width = view.viewWidth
    height = view.viewHeight

    pixel_x = width/imgSize[0]
    pixel_y = height/imgSize[1]
    sizeX = imgSize[0]
    sizeY = imgSize[1]
    
    img_tmp = np.zeros((imgSize[1], imgSize[0], 3), dtype=np.uint8)
    for i in np.arange(imgSize[1]):
        for j in np.arange(imgSize[0]):
            u = pixel_x*(j-sizeX/2-0.5)
            v = pixel_y*(i-sizeY/2-0.5)
            pixel_on_img_plane = view_point + u*u_unit + v*v_unit - dist_img_plane*w_unit  # s
            direction = pixel_on_img_plane-view_point
            t, surface_idx, blocked = doRayTracing(view_point, direction, surfaces)  # rayTracing

            if blocked:
                temp = shadow(view_point, pixel_on_img_plane, t,
                              surface_idx, lights, surfaces, view)
                result = Color(temp[0], temp[1], temp[2])
            else:
                result = Color(BLACK[0], BLACK[1], BLACK[2])
            result.gammaCorrect(2.2)
            img_tmp[i][j] = result.toUINT8()

    return img_tmp


def shadow(start_point, direction_point, t, surface_idx, lights, surfaces, view):
    result = np.array([0, 0, 0]).astype(np.float_)
    view_point = view.viewPoint

    d = direction_point - start_point

    surface_point = start_point + t*d
    shadRay_start_point = surface_point

    for light in lights:
        direction = -makeUnitVector(light.position-shadRay_start_point)
        check_t, check_idx, blocked = doRayTracing(shadRay_start_point, direction, surfaces)

        if blocked and surface_idx == check_idx:
            surface = surfaces[surface_idx]
            result += doShading(surface_point, view_point, light, surface)

    return result


# Find "t" such that r(t) = p + td & idx of surfaces
def doRayTracing(start_point, direction, surfaces):
    d = direction
    ret_t = INF    # t of r(t) = p + td
    ret_idx = -1    # idx of surfaces
    for idx, surface in enumerate(surfaces):
        if surface.__class__.__name__ == 'Sphere':
            p = start_point - surface.center

            dp = np.dot(d, p)
            dd = np.dot(d, d)
            pp = np.dot(p, p)

            D = dp**2 - dd*(pp - surface.radius**2)
            if D < 0:    # There is no Intersection
                continue
            elif D >= 0:
                t1 = (-dp - np.sqrt(D))/dd
                t2 = (-dp + np.sqrt(D))/dd
                if ret_t >= t2:
                    ret_t = t2
                    ret_idx = idx
                if ret_t >= t1:
                    ret_t = t1
                    ret_idx = idx

    if ret_idx != -1:
        is_blocked = True
    else:
        is_blocked = False
    return (ret_t, ret_idx, is_blocked)


def doShading(surface_point, view_point, light, surface):
    surface_to_light = makeUnitVector(light.position - surface_point)
    surface_to_view = makeUnitVector(view_point - surface_point)
    surface_normal = makeUnitVector(surface_point - surface.center)

    if surface.shader.__class__.__name__ == "ShaderPhong":
        result = shadePhong(surface_to_light, surface_to_view, surface_normal, surface, light)

    elif surface.shader.__class__.__name__ == "ShaderLambertian":
        result = shadeLambertian(surface_to_light, surface_normal, surface, light)

    return result


def shadeLambertian(to_light, normal, surface, light):
    result = np.array([0, 0, 0]).astype(np.float_)
    result[0] = result[0] + surface.shader.diffuse[0] * light.intensity[0] * max(0, np.dot(to_light, normal))
    result[1] = result[1] + surface.shader.diffuse[1] * light.intensity[1] * max(0, np.dot(to_light, normal))
    result[2] = result[2] + surface.shader.diffuse[2] * light.intensity[2] * max(0, np.dot(to_light, normal))
    return result
    # return color


def shadePhong(to_light, to_view, normal, surface, light):
    result = np.array([0, 0, 0]).astype(np.float_)
    h = makeUnitVector(to_light + to_view)

    result[0] = result[0] + ambient[0] + surface.shader.diffuse[0] * light.intensity[0] * max(0, np.dot(normal, to_light)) \
        + surface.shader.specular[0] * light.intensity[0] * np.power(max(0, np.dot(normal, h)), surface.shader.exponent[0])
    
    result[1] = result[1] + ambient[1] + surface.shader.diffuse[1] * light.intensity[1] * max(0, np.dot(normal, to_light)) \
        + surface.shader.specular[1] * light.intensity[1] * np.power(max(0, np.dot(normal, h)), surface.shader.exponent[0])
    
    result[2] = result[2] + ambient[2] + surface.shader.diffuse[2] * light.intensity[2] * max(0, np.dot(normal, to_light)) \
        + surface.shader.specular[2] * light.intensity[2] * np.power(max(0, np.dot(normal, h)), surface.shader.exponent[0])
    
    return result


if __name__ == "__main__":
    main()
