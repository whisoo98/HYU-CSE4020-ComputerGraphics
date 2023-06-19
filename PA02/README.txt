Project Assignment #2 Cow Roller Coaster

2018008240 Kim Whisoo

I. UI Implementation

1. Camera
If “c” or “space bar” is pressed, the camera is changed
If a number in range from 0 to 4 is pressed, alter the camera corresponding the number.

2. Click
The "Click" is combined with two actions that mouse goes DOWN and goes UP.
There are some cases to handle several actions.
If the right mouse is clicked on anywhere, the position of cursor will be printed on the terminal and the work of Cow Roller Coaster will be resetted for making easy to re-drawing.
If the left mouse is clicked on anywhere except cow, nothing happen.
If the left mouse is clicked and cow is attached(drag), in the screen, the cow is drawn additionally at that point. 
To be clear, the cow is added on screen when the left mouse is UP. Until there are six cows in the screen except attached cow on cursor, the roller coaster will not start.
If there are six cows, cow will ride roller coaster following B spline curve of points that you've clicked, and after 3 times rotation the cow will go back to the initial mode with the turning head.

3. Drag
The "Drag" is state of the mouse keep being DOWN.
In "Drag" state, the cow's position can be changed vertically following cursor.
If the left mouse is clicked on cow and it is the first click on cow, the the cow is attached to cursor.
In this condition, the cow will be moved horizotally following cursor.


II. Added Variables & Functions

1. Added Variables
- save_cows
  This is a list to save clicked cow's position. They are appended sequentailly.

- animStartTime
  This is a Variable with two rolls.
  If it is None, it represent the cow is not attached to cursor.
  If the cow is attached to cursor, then it is set to 0.
  The value 0, it represent that the cow is not drawn. After cow is drawn it is set to timestamp of clicked.

- anime_start
  This is a boolean Variable to block interrupt such as click while cow rides roller coaster.

- t
  This is a variable to have same time interval between save_cows[i] and save_cows[i+1].
  Each (save_cows) interval, it is rendered 60 times.

- i
  This is a index variable for save_cows list.

- k
  This is a variable to check 3 times roller coaster rotation.

- timedelta
  This is a variable to make each interval rendered 60 times.
  It is 0.016667

- before_mulMat
  This is a variable to save cow position just before timedelta.

- cursor_click_pos
  This is a variable to save cow's vertical position while verticalled draging.

- rided
  This is a variable to save how many times cow rides roller coaster.
  The reason why needed is after first riding cow shouled be turned.

- right_click
  This is a variable to dertemine the function, it will be shown below, resetRollerCoaster() is called from right click or from 3 times roller coaster rotation.

2. Added Funtions

- resetRollerCoaster()
  This function reset all the variables involved with Cow Roller Coaster to make initial state, execpt cow's heading.

- uXu(), uX()
  This functions used to make Cubic B-spline Matrix.

- norm2()
  This fuction return norm-2 of vector.

- yaw_rotation(), pitch_rotation()
  This functions make rotation matrix with each rotataion-axis.
  Inside, I do vector calculation referenced viedo lecture.
  To decide angle is in [0,pi] or [pi, 2pi], I use cross product and check the direction.

- displayRollerCoaster()
  This is a display function to separate display() which represent stopped cow, while it render cow roller coaster.
  It calculates B-Spline Matrix, yaw rotation matrix and pitch rotation matrix and multiplies them to render cow.

 
III. Implementation Explain

1. Drag
When dragging, the cow should be attached to the mouse cursor. I modified onMouseButton() and onMouseDrag().
In specific, these are what I modified.
- IsDrag variable is 0 only in initial state.
- If the cow is clicked in inital state which means first click, isDrag is either V_DRAG or H_DRAG.
- To do vertical dragging, I saved the clicked cow's position and using it, cow is fixed horizontally.

2. B-spline
  I calculated the Cubic B-spline using hard coding.
  In Lecture Spline, I coded each Matrix manually.

3. Yaw and Pitch Rotation
This is the most difficult part of this assignment.
To be honest, still I can't handle exact cows heading, floating calculation error of vector angle.
The details of functions are in the video lecture that to figure out what is the vector I want to rotate, So I skip over that part.
But the things need to think are how to express angle ranged between [pi, 2pi].
Because the arc trigonometric functions in python library such as numpy or math are able to represent [0, pi].
I can solve this problem using cross-product and compare it is same direction with rotation-axis.
However, because of numerical error, there are some cases that can't render the cow literally. He is gone somewhere and just came out.
And I multiply these matrix with cow's B-Spline Matrix.

4. Uniform Rendering
Each cow points interval, I want to express that uniformly which means that they spend same time no matter how the distance between cow points are.
It is a consider that how many steps do I need.
If the step is too small, it is hard to compute exact Spline matrix.
If the step is too big, it is not looks like a curve.
I splited each interval with 60 steps to follow 60Hz.

