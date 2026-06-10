import os
import django
import random
from datetime import datetime, timedelta
from django.utils import timezone

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from educlubs.models import (
    Section, Level, Subject, Topic, Subtopic, Lesson, Assessment,
    Club, Note, RoleModel, PracticalProject, DiscussionMessage,
    Question, Choice
)

def get_s2_detailed_notes(subject, topic, lesson):
    notes = {}
    
    # Mathematics
    notes["Mathematics"] = {
        "Solving Linear Equations": r"""### 1. Introduction to Linear Equations
A **linear equation** is an algebraic equation of the first degree (the highest exponent of the variables is 1). It represents a straight line when plotted on a Cartesian plane. In Senior 2 Mathematics, mastering linear equations is the foundation for solving simultaneous equations, coordinate geometry, and linear programming.

#### Core Definitions:
- **Variable**: A letter representing an unknown quantity (e.g., $x$, $y$).
- **Coefficient**: The numerical factor multiplying a variable (e.g., in $5x$, $5$ is the coefficient).
- **Constant**: A fixed number that does not change (e.g., $+7$, $-12$).

---

### 2. The Golden Rule of Equation Solving
To solve a linear equation, you must isolate the variable on one side of the equals sign. Whatever operation you perform on one side, **you must perform the exact same operation on the other side** to keep the equation balanced.

#### Core Methods:
1. **Transposition (Balancing Method)**:
   - Move all variable terms to one side (usually LHS) and all constant terms to the other side (usually RHS).
   - When a term crosses the equals sign, its sign changes:
     - Addition ($+$) becomes Subtraction ($-$).
     - Subtraction ($-$) becomes Addition ($+$).
     - Multiplication ($\times$) becomes Division ($\div$).
     - Division ($\div$) becomes Multiplication ($\times$).
2. **Clearing Brackets (Distribution)**:
   - Use the distributive law $a(b + c) = ab + ac$ to remove parentheses before rearranging terms.
3. **Clearing Fractions (LCM Method)**:
   - If the equation contains fractions, find the Least Common Multiple (LCM) of all denominators.
   - Multiply every term on both sides of the equation by this LCM to eliminate fractions completely.

---

### 3. Step-by-Step Worked Examples

#### Example 1: Basic Transposition
Solve for $x$:
$$3x - 7 = 14$$

*Step 1: Move the constant $-7$ to the right-hand side. It changes to $+7$.*
$$3x = 14 + 7$$
$$3x = 21$$

*Step 2: Divide both sides by the coefficient of $x$, which is 3.*
$$x = \frac{21}{3}$$
$$x = 7$$

#### Example 2: Dealing with Brackets
Solve for $y$:
$$4(2y - 3) = 2(y + 9)$$

*Step 1: Expand the brackets on both sides.*
$$8y - 12 = 2y + 18$$

*Step 2: Transpose the variable terms to the LHS and constant terms to the RHS.*
$$8y - 2y = 18 + 12$$
$$6y = 30$$

*Step 3: Isolate $y$ by dividing by 6.*
$$y = \frac{30}{6}$$
$$y = 5$$

#### Example 3: Clearing Fractions
Solve for $x$:
$$\frac{2x - 3}{4} - \frac{x - 1}{3} = \frac{1}{6}$$

*Step 1: Find the LCM of the denominators (4, 3, and 6), which is 12.*
*Step 2: Multiply every single term by 12.*
$$12 \left(\frac{2x - 3}{4}\right) - 12 \left(\frac{x - 1}{3}\right) = 12 \left(\frac{1}{6}\right)$$
$$3(2x - 3) - 4(x - 1) = 2$$

*Step 3: Expand brackets. Be very careful with the negative sign!*
$$6x - 9 - 4x + 4 = 2$$
$$2x - 5 = 2$$

*Step 4: Solve for $x$.*
$$2x = 2 + 5$$
$$2x = 7$$
$$x = \frac{7}{2} = 3.5$$

#### Example 4: Word Problem Translation
A rectangle's length is $5\text{ cm}$ longer than twice its width. If the perimeter is $46\text{ cm}$, find its dimensions.

*Step 1: Let the width be $w$ cm. Thus, the length is $2w + 5$ cm.*
*Step 2: Use the perimeter formula $P = 2(\text{length} + \text{width})$.*
$$46 = 2((2w + 5) + w)$$
$$46 = 2(3w + 5)$$

*Step 3: Divide both sides by 2.*
$$23 = 3w + 5$$

*Step 4: Transpose and solve for $w$.*
$$3w = 23 - 5$$
$$3w = 18 \implies w = 6\text{ cm}$$

*Step 5: Calculate the length.*
$$\text{Length} = 2(6) + 5 = 17\text{ cm}$$
*Dimensions: Width = $6\text{ cm}$, Length = $17\text{ cm}$.*

---

### 4. NCDC Exam Practice Questions
1. **Question**: Solve the equation: $\frac{5x - 2}{3} - \frac{x + 3}{2} = 1$
   *Hint: The LCM is 6. Multiply both sides and solve.*
2. **Question**: Two consecutive odd integers sum to $136$. Find the two integers.
   *Hint: Let the integers be $n$ and $n + 2$. Write the equation and solve.*
3. **Question**: Solve for $a$: $3(a - 4) - (a + 2) = 2(a - 7)$
   *Observe what happens to the variable $a$. Show your steps clearly.*
""",
        "Elimination & Substitution Methods": r"""### 1. What are Simultaneous Equations?
A pair of simultaneous equations consists of two linear equations with two unknown variables (typically $x$ and $y$). To solve them simultaneously means to find a single ordered pair $(x, y)$ that satisfies both equations at the same time. Geometrically, this represents the **point of intersection** of two straight lines on a graph.

---

### 2. Method 1: The Elimination Method
The goal of this method is to eliminate one of the variables by adding or subtracting the equations. This leaves a single equation with one variable, which is easy to solve.

#### Step-by-Step Guide:
1. Arrange both equations in the form $Ax + By = C$.
2. Multiply one or both equations by suitable numbers so that the coefficients of one variable (either $x$ or $y$) have the same numerical value.
3. If the signs of the matching coefficients are:
   - **Opposite** (one positive, one negative): **ADD** the two equations.
   - **Same** (both positive or both negative): **SUBTRACT** the equations.
4. Solve the resulting single-variable equation.
5. Substitute the found value back into either of the original equations to solve for the other variable.

#### Worked Example (Elimination):
Solve the system:
1)  $2x + 3y = 12$
2)  $x - y = 1$

*Step 1: Multiply Equation (2) by 3 so that the coefficients of $y$ match (we will have $+3y$ in Eq 1 and $-3y$ in Eq 3).*
$$3(x - y) = 3(1) \implies 3x - 3y = 3 \quad \text{(Equation 3)}$$

*Step 2: Add Equation (1) and Equation (3) because the coefficients of $y$ (+3 and -3) have opposite signs.*
$$(2x + 3y) + (3x - 3y) = 12 + 3$$
$$5x = 15$$
$$x = 3$$

*Step 3: Substitute $x = 3$ into Equation (2) to find $y$.*
$$3 - y = 1 \implies y = 2$$
**Solution: $x = 3, y = 2$ or $(3, 2)$**

---

### 3. Method 2: The Substitution Method
This method involves expressing one variable in terms of the other using one equation, and then substituting that expression into the second equation.

#### Step-by-Step Guide:
1. Choose one equation and make one variable the subject (e.g., $x = \text{expression in } y$).
2. Substitute this expression into the **other** equation.
3. Solve the resulting single-variable equation.
4. Substitute the solved value back into your expression from Step 1 to find the second variable.

#### Worked Example (Substitution):
Solve the system:
1)  $3x + 2y = 16$
2)  $2x - y = 6$

*Step 1: Express $y$ in terms of $x$ from Equation (2) since it has a coefficient of $-1$.*
$$2x - y = 6 \implies y = 2x - 6 \quad \text{(Equation 3)}$$

*Step 2: Substitute Equation (3) into Equation (1).*
$$3x + 2(2x - 6) = 16$$
$$3x + 4x - 12 = 16$$
$$7x - 12 = 16$$

*Step 3: Solve for $x$.*
$$7x = 28 \implies x = 4$$

*Step 4: Substitute $x = 4$ back into Equation (3).*
$$y = 2(4) - 6 = 8 - 6 = 2$$
**Solution: $x = 4, y = 2$ or $(4, 2)$**

---

### 4. Real-World Applications (Word Problems)
Many practical situations can be modeled using simultaneous equations.

#### Example: Animals on a Farm
A farmer has chickens and goats. The total number of animals is 35, and the total number of legs is 110. Find the number of chickens and goats.

*Step 1: Define variables.*
- Let the number of chickens be $c$.
- Let the number of goats be $g$.

*Step 2: Set up equations.*
- Total animals: $c + g = 35$ (Equation 1)
- Total legs (chickens have 2 legs, goats have 4 legs): $2c + 4g = 110$ (Equation 2)

*Step 3: Solve using substitution.*
From Equation (1), $c = 35 - g$.
Substitute into Equation (2):
$$2(35 - g) + 4g = 110$$
$$70 - 2g + 4g = 110$$
$$70 + 2g = 110$$
$$2g = 40 \implies g = 20$$

Substitute $g = 20$ back to find $c$:
$$c = 35 - 20 = 15$$
**Solution: The farmer has 15 chickens and 20 goats.**

---

### 5. NCDC Exam Practice Questions
1. **Question**: Solve the following simultaneous equations:
   $$5x - 2y = 19$$
   $$3x + 4y = 1$$
2. **Question**: The sum of two numbers is 47 and their difference is 15. Formulate two equations and solve them to find the two numbers.
3. **Question**: At a school canteen, 3 sodas and 2 buns cost UGX 7,500. 5 sodas and 4 buns cost UGX 13,500. Find the cost of a single soda and a single bun.
""",
        "Angle Properties of Circles": r"""### 1. Circle Geometry Fundamentals
In Senior 2 Circle Geometry, we study the relationships between angles subtended by arcs, chords, and tangents. These properties are described in terms of several key theorems.

#### Terminology:
- **Arc**: A portion of the circle's circumference.
- **Chord**: A straight line segment connecting two points on the circumference.
- **Segment**: The area enclosed between a chord and an arc. The larger area is the **major segment**, and the smaller is the **minor segment**.
- **Cyclic Quadrilateral**: A four-sided polygon whose vertices all lie on the circumference of a circle.
- **Tangent**: A straight line that touches the circle at exactly one point.

---

### 2. Core Circle Theorems

#### Theorem 1: Angle at Center and Circumference
The angle subtended by an arc at the center of a circle is **twice** the angle subtended by the same arc at any point on the circumference.
$$\theta_{\text{center}} = 2 \times \theta_{\text{circumference}}$$

#### Theorem 2: Angles in the Same Segment
Angles subtended by the same arc (or chord) in the same segment of a circle are **equal**.
$$\angle APB = \angle AQB$$

#### Theorem 3: Angle in a Semicircle
The angle subtended by a diameter at the circumference is always a right angle ($90^\circ$).

#### Theorem 4: Cyclic Quadrilateral Theorem
The opposite angles of a cyclic quadrilateral sum up to $180^\circ$ (they are supplementary).
$$\angle A + \angle C = 180^\circ \quad \text{and} \quad \angle B + \angle D = 180^\circ$$

#### Theorem 5: Tangent-Radius Theorem
A tangent to a circle is perpendicular to the radius at the point of contact ($90^\circ$).

#### Theorem 6: Alternate Segment Theorem
The angle between a tangent and a chord through the point of contact is equal to the angle in the alternate segment.

---

### 3. Worked Examples

#### Example 1: Finding Angle at Circumference
*Problem*: In a circle with center $O$, points $A$ and $B$ lie on the circumference. The angle $AOB$ at the center is $130^\circ$. Find the angle $APB$ where $P$ is a point on the major arc.

*Solution*: According to Theorem 1, the angle subtended at the center is twice the angle subtended at the circumference.
$$\angle APB = \frac{1}{2} \times \angle AOB$$
$$\angle APB = \frac{130^\circ}{2} = 65^\circ$$

#### Example 2: Cyclic Quadrilateral Calculation
*Problem*: $ABCD$ is a cyclic quadrilateral. If $\angle ABC = 85^\circ$ and $\angle BCD = 105^\circ$, find the angles $\angle ADC$ and $\angle DAB$.

*Solution*: By Theorem 4, opposite angles sum to $180^\circ$.
$$\angle ADC = 180^\circ - \angle ABC = 180^\circ - 85^\circ = 95^\circ$$
$$\angle DAB = 180^\circ - \angle BCD = 180^\circ - 105^\circ = 75^\circ$$

---

### 4. NCDC Exam Practice Questions
1. **Question**: In a circle with center $O$, a chord $XY$ subtends an angle $XOY = 100^\circ$ at the center. Find the angle $XPY$ on:
   - a) The major arc.
   - b) The minor arc. (Hint: Recall that the reflex angle at the center subtends the angle on the minor arc).
2. **Question**: Prove that the angle in a semicircle is a right angle using the center angle theorem.
3. **Question**: A tangent $PQ$ touches a circle at $T$. The center of the circle is $O$. A point $R$ lies on the circumference such that $\angle OTR = 35^\circ$. Find the angle $\angle PT\text{R}$.
"""
    }

    # Physics
    notes["Physics"] = {
        "Inertia & Newton's First Law": r"""### 1. Introduction to Force and Motion
In Senior 2 Physics, we study how forces cause or modify motion. The foundation of mechanics is laid by Sir Isaac Newton's three laws of motion.

#### Core Concepts:
- **Force ($F$)**: A push or pull acting upon an object as a result of its interaction with another object. Measured in **Newtons ($N$)**.
- **Mass ($m$)**: The quantity of matter in a body. It is a scalar quantity measured in **kilograms ($kg$)**. Crucially, mass is a direct measure of a body's inertia.
- **Inertia**: The natural tendency of a body to resist any change in its state of rest or uniform motion in a straight line.

---

### 2. Newton's First Law of Motion (Law of Inertia)
Newton's First Law states that:
> **A body remains in its state of rest or uniform motion in a straight line unless acted upon by a net (resultant) external force.**

This means that if the net force on an object is zero, an object at rest will stay at rest, and a moving object will continue to move at a constant speed in a straight line.

#### Galileo's Thought Experiment:
Galileo Galilei paved the way for this law by demonstrating that a ball rolling down a frictionless inclined plane would roll up an opposing plane to the exact same height. If the second plane was horizontal and infinitely long, the ball would roll forever with constant velocity, trying to reach its original height, because no friction (opposing force) acts on it.

---

### 3. Mass vs. Weight: A Critical Distinction
Many students confuse mass and weight. In physics, they are distinct physical quantities:

| Feature | Mass | Weight |
| :--- | :--- | :--- |
| **Definition** | Amount of matter in an object | Gravitational force acting on an object |
| **SI Unit** | Kilogram ($kg$) | Newton ($N$) |
| **Quantity Type** | Scalar (has magnitude only) | Vector (has magnitude and acts downwards) |
| **Constancy** | Constant everywhere in the universe | Varies depending on gravitational field strength ($W=mg$) |
| **Measurement** | Beam balance | Spring balance |

---

### 4. Real-World Applications of Inertia

#### A. Passengers in a Vehicle:
- **Sudden Braking**: When a moving bus brakes suddenly, the passengers' feet stop moving because they are in contact with the bus floor. However, their upper bodies continue moving forward at the previous speed due to inertia. This causes them to fall forward.
- **Sudden Start**: When a stationary bus accelerates forward suddenly, the passengers' lower bodies move forward with the bus, but their upper bodies remain at rest due to inertia, causing them to lurch backward.

#### B. Safety Features in Automobiles:
- **Seatbelts**: Hold passengers in place, applying a backward force to stop them from flying forward during a sudden collision.
- **Headrests**: Prevent whiplash injuries. When a car is hit from behind, it accelerates forward suddenly. The headrest pushes the passenger's head forward along with their torso, preventing the head from snapping backward due to inertia.

#### C. Other Examples:
- **Shaking a fruit tree**: Shaking a branch causes the branch to move back and forth quickly. The fruits, due to their inertia, tend to remain at rest, causing the stems to snap and the fruits to fall.
- **Tightening a hammer head**: Striking the bottom of a hammer handle vertically down on a anvil or bench causes the handle to stop suddenly on impact. The heavy iron head, possessing large inertia, continues moving downwards, forcing itself tightly onto the wooden handle.

---

### 5. NCDC Exam Practice Questions
1. **Question**: State Newton's First Law of Motion and define the term *Inertia*.
2. **Question**: Explain why a person running at high speed cannot stop immediately at the finish line.
3. **Question**: A block of mass $5\text{ kg}$ is resting on a frictionless table. If no net force acts on it, describe its state of motion. If a net force of $0\text{ N}$ acts on it while it is moving at $2\text{ m/s}$, describe its state of motion.
""",
        "Force & Newton's Second Law ($F = ma$)": r"""### 1. Linear Momentum
Before stating Newton's Second Law, we must define **linear momentum**, which describes the quantity of motion in a moving body.

#### Definition:
**Linear momentum ($p$)** is the product of a body's mass ($m$) and its velocity ($v$).
$$p = mv$$
- **SI Unit**: Kilogram-meter per second ($kg\cdot m/s$) or Newton-second ($N\cdot s$).
- **Quantity Type**: Vector quantity (acts in the direction of the velocity).

---

### 2. Newton's Second Law of Motion
Newton's Second Law states that:
> **The rate of change of momentum of a body is directly proportional to the applied force and takes place in the direction of the force.**

#### Derivation of $F = ma$:
Let a body of mass $m$ have an initial velocity $u$. A constant force $F$ acts on it for a time $t$, changing its velocity to $v$.
1. Initial momentum: $p_i = mu$
2. Final momentum: $p_f = mv$
3. Change in momentum: $\Delta p = mv - mu = m(v - u)$
4. Rate of change of momentum: $\frac{\Delta p}{t} = \frac{m(v - u)}{t}$

According to the law:
$$F \propto \frac{m(v - u)}{t}$$

Since acceleration $a = \frac{v - u}{t}$:
$$F \propto ma \implies F = k \cdot ma$$

Where $k$ is a constant of proportionality. In the SI system, the unit of force (the Newton) is defined such that $k = 1$.
$$\mathbf{F = ma}$$

#### Definition of a Newton (N):
One Newton is the force that gives a mass of $1\text{ kg}$ an acceleration of $1\text{ m/s}^2$.

---

### 3. Momentum, Force, and Impulse
- **Impulse**: The product of the applied force ($F$) and the time ($t$) for which it acts.
$$\text{Impulse} = F \times t = \Delta p = m(v - u)$$
- **SI Unit**: Newton-second ($N\cdot s$) or $kg\cdot m/s$.
- **Application**: Landing on a foam mattress. When a high jumper lands on foam, the mattress deforms, increasing the time ($t$) of impact. Because $F = \frac{\Delta p}{t}$, a larger time $t$ reduces the force $F$ experienced by the jumper, preventing injury.

---

### 4. Worked Calculation Problems

#### Example 1: Simple Force Calculation
Calculate the force required to accelerate a body of mass $8\text{ kg}$ at $3.5\text{ m/s}^2$.

*Solution*:
$$F = ma = 8\text{ kg} \times 3.5\text{ m/s}^2 = 28\text{ N}$$

#### Example 2: Force and Change of Velocity
A trolley of mass $12\text{ kg}$ is traveling at $4\text{ m/s}$. A force is applied for $3\text{ seconds}$, increasing its velocity to $10\text{ m/s}$. Calculate the magnitude of the force.

*Solution*:
$$a = \frac{v - u}{t} = \frac{10 - 4}{3} = \frac{6}{3} = 2\text{ m/s}^2$$
$$F = ma = 12\text{ kg} \times 2\text{ m/s}^2 = 24\text{ N}$$

#### Example 3: Resultant Force with Friction
A wooden block of mass $5\text{ kg}$ is pulled along a rough horizontal table by a horizontal force of $18\text{ N}$. If the frictional force opposing the motion is $3\text{ N}$, find the acceleration of the block.

*Solution*:
*Step 1: Calculate the net (resultant) force ($F_{\text{net}}$).*
$$F_{\text{net}} = \text{Pulling Force} - \text{Friction}$$
$$F_{\text{net}} = 18\text{ N} - 3\text{ N} = 15\text{ N}$$

*Step 2: Apply Newton's Second Law ($F_{\text{net}} = ma$).*
$$15 = 5 \times a \implies a = \frac{15}{5} = 3\text{ m/s}^2$$

#### Example 4: Decelerating Force
A car of mass $1000\text{ kg}$ traveling at $20\text{ m/s}$ is brought to rest in a distance of $50\text{ meters}$ by its brakes. Find the average braking force.

*Solution*:
*Step 1: Find acceleration using the equations of motion: $v^2 = u^2 + 2as$.*
Here, $u = 20\text{ m/s}$, $v = 0\text{ m/s}$, and $s = 50\text{ m}$.
$$0^2 = 20^2 + 2(a)(50)$$
$$0 = 400 + 100a \implies 100a = -400 \implies a = -4\text{ m/s}^2 \quad \text{(deceleration)}$$

*Step 2: Calculate braking force.*
$$F = ma = 1000\text{ kg} \times (-4\text{ m/s}^2) = -4000\text{ N}$$
*(The negative sign shows that the force is opposing the direction of motion. The magnitude is $4000\text{ N}$.)*

---

### 5. NCDC Exam Practice Questions
1. **Question**: Define the terms *linear momentum* and *impulse*. State their SI units.
2. **Question**: State Newton's Second Law of Motion. Show how it leads to the formula $F = ma$.
3. **Question**: A bullet of mass $20\text{ g}$ ($0.02\text{ kg}$) is fired from a gun with a speed of $300\text{ m/s}$. If it penetrates a sandbag and comes to rest in $0.05\text{ seconds}$, calculate:
   - a) The deceleration of the bullet.
   - b) The average retarding force exerted by the sand.
""",
        "Action & Reaction (Third Law)": r"""### 1. Statement of Newton's Third Law
Newton's Third Law of Motion states that:
> **To every action, there is an equal and opposite reaction.**

This means that forces always occur in **pairs**. If Object A exerts a force on Object B (action), Object B simultaneously exerts an equal and opposite force on Object A (reaction).

$$\mathbf{F_{\text{A on B}} = -F_{\text{B on A}}}$$

#### Essential Characteristics of Action-Reaction Pairs:
1. **Equal Magnitude**: The two forces are exactly equal in size.
2. **Opposite Direction**: One force acts in the opposite direction of the other.
3. **Act on Different Bodies**: The action force acts on one body, while the reaction force acts on the other. **This is why they do not cancel each other out!** They cannot produce equilibrium because they act on different objects.
4. **Same Type of Force**: If the action is a contact force, the reaction is also a contact force. If the action is gravitational, the reaction is also gravitational.

---

### 2. Practical Applications and Explanations

#### A. Recoil of a Gun
When a gun fires a bullet, the gun exerts a forward force on the bullet (action), which accelerates the bullet forward. In return, the bullet exerts an equal and opposite backward force on the gun (reaction). This causes the gun to kick backward, which is known as **recoil**.
- **Conservation of Momentum Calculation**:
  $$\text{Momentum before firing} = 0$$
  $$\text{Momentum after firing} = M_g V_g + m_b v_b = 0 \implies V_g = -\frac{m_b v_b}{M_g}$$
  Where $M_g$ and $V_g$ are mass and velocity of the gun, and $m_b$ and $v_b$ are mass and velocity of the bullet. The negative sign shows the gun moves backward.

#### B. Walking on the Ground
When you walk, your foot pushes backward and downward on the ground (action). By Newton's Third Law, the ground exerts an equal and opposite forward and upward force on your foot (reaction). This reaction force pushes you forward.
*Note: If you try to walk on slippery ice, friction is low. Your foot cannot push backward on the ice, so the ice cannot push you forward, making walking difficult.*

#### C. Rocket and Jet Propulsion
Inside a rocket engine, fuel burns rapidly to produce high-pressure gas. The rocket nozzle pushes the hot exhaust gases downward at high speed (action). In response, the escaping gases exert an equal and opposite upward force on the rocket (reaction). This upward force (thrust) propels the rocket into space.

#### D. Swimming
A swimmer pushes the water backward using their hands and feet (action). The water simultaneously exerts an equal and opposite forward force on the swimmer (reaction), moving them forward through the pool.

---

### 3. Common Misconception: Book on a Table
Consider a book resting on a horizontal table.
- The earth pulls the book downwards with gravity (Weight, $W$).
- The table pushes the book upwards with a Normal Reaction force ($R$).
- Since the book is in equilibrium, $R = W$.

*Is this an Action-Reaction pair?* **NO!**
1. Both forces act on the **same body** (the book). Action-reaction pairs must act on different bodies.
2. They are of **different types**: Weight is a gravitational force, while the normal reaction is an electromagnetic contact force.
3. *The real pairs are*:
   - Earth pulls book down (gravity) $\leftrightarrow$ Book pulls Earth up (gravity).
   - Book pushes table down (contact) $\leftrightarrow$ Table pushes book up (contact).

---

### 4. NCDC Practice Questions
1. **Question**: State Newton's Third Law of Motion and outline three characteristics of action-reaction pairs.
2. **Question**: Explain, with the aid of a diagram or step-by-step forces, how a helicopter is able to lift off the ground.
3. **Question**: A gun of mass $4\text{ kg}$ fires a bullet of mass $0.05\text{ kg}$ with a muzzle velocity of $200\text{ m/s}$. Calculate the recoil velocity of the gun.
""",
        "Work Done & Calculations": r"""### 1. Scientific Concept of Work
In everyday language, "work" means any physical or mental effort. In physics, however, **work** has a precise mathematical definition.

#### Definition:
**Work is done** only when a force applied to an object causes it to undergo a displacement in the direction of the force.
$$Work = Force \times Displacement$$
$$\mathbf{W = F \times d}$$

- **SI Unit**: Newton-meter ($N\cdot m$), which is defined as the **Joule ($J$)**.
- **Definition of 1 Joule**: One Joule is the work done when a force of $1\text{ Newton}$ moves an object through a distance of $1\text{ meter}$ in the direction of the force.
- **Quantity Type**: Scalar quantity.

#### When is Work Done Equal to Zero?
Work done is zero in the following cases:
1. **No displacement**: If you push against a concrete wall with a force of $500\text{ N}$ for hours but the wall does not move ($d = 0$), the work done is $0\text{ J}$.
2. **Perpendicular displacement**: If the force applied is perpendicular ($90^\circ$) to the direction of motion. For example, a student carrying a heavy suitcase on their head while walking horizontally does no work *against gravity* because the upward supporting force is perpendicular to the horizontal displacement.

---

### 2. Energy and its Forms
**Energy** is defined as the ability or capacity to do work. It is also measured in **Joules ($J$)**.

#### A. Gravitational Potential Energy ($E_p$ or GPE)
The energy stored in an object due to its vertical position above the ground.
$$\mathbf{E_p = mgh}$$
Where:
- $m$ is mass ($kg$)
- $g$ is gravitational acceleration ($10\text{ m/s}^2$ on Earth)
- $h$ is vertical height ($m$)

#### B. Kinetic Energy ($E_k$ or KE)
The energy possessed by a body due to its motion.
$$\mathbf{E_k = \frac{1}{2}mv^2}$$
Where $v$ is the speed of the body ($m/s$).

#### C. Law of Conservation of Mechanical Energy
In a closed, frictionless system, energy cannot be created or destroyed, only transformed from one form to another.
$$\text{Total Mechanical Energy} = E_p + E_k = \text{Constant}$$
For a falling object: $\text{Loss in } E_p = \text{Gain in } E_k$.

---

### 3. Power
**Power ($P$)** is defined as the rate of doing work or the rate at which energy is converted.
$$Power = \frac{Work\ Done}{Time\ Taken} = \frac{W}{t}$$
- **SI Unit**: Joule per second ($J/s$), which is called the **Watt ($W$)**.
- **Definition of 1 Watt**: One Watt is a rate of working of $1\text{ Joule per second}$.
- **Alternative Formula**: Since $W = F \times d$, then $P = \frac{F \times d}{t} = F \times v$ (Force $\times$ Velocity).

---

### 4. Worked Calculations

#### Example 1: Work Done lifting against Gravity
A crane lifts a load of mass $250\text{ kg}$ vertically upwards through a height of $8\text{ meters}$ in $20\text{ seconds}$. Calculate:
- a) The work done against gravity. (Take $g = 10\text{ m/s}^2$)
- b) The power output of the crane.

*Solution*:
- a) Work Done = Force $\times$ Distance = Weight $\times$ Height
  $$\text{Force (Weight)} = mg = 250\text{ kg} \times 10\text{ m/s}^2 = 2500\text{ N}$$
  $$W = F \times h = 2500\text{ N} \times 8\text{ m} = 20,000\text{ J} \quad (20\text{ kJ})$$
- b) Power:
  $$P = \frac{W}{t} = \frac{20,000\text{ J}}{20\text{ s}} = 1000\text{ W} \quad (1\text{ kW})$$

#### Example 2: Kinetic Energy
Calculate the kinetic energy of a motorcycle of mass $150\text{ kg}$ traveling at a constant speed of $20\text{ m/s}$.

*Solution*:
$$E_k = \frac{1}{2}mv^2 = \frac{1}{2} \times 150\text{ kg} \times (20\text{ m/s})^2$$
$$E_k = 75 \times 400 = 30,000\text{ J} \quad (30\text{ kJ})$$

#### Example 3: Conservation of Energy
A stone of mass $2\text{ kg}$ is dropped from the top of a building which is $45\text{ m}$ high. Calculate its kinetic energy just before hitting the ground. (Neglect air resistance, $g = 10\text{ m/s}^2$).

*Solution*:
By the law of conservation of energy, the kinetic energy just before impact is equal to the gravitational potential energy at the top of the building.
$$E_k = E_p = mgh$$
$$E_k = 2\text{ kg} \times 10\text{ m/s}^2 \times 45\text{ m} = 900\text{ J}$$

---

### 5. NCDC Exam Practice Questions
1. **Question**: State the scientific definition of *work* and explain two scenarios where work done is zero despite a force being applied.
2. **Question**: Define *power* and show that $Power = Force \times Velocity$.
3. **Question**: A girl of mass $45\text{ kg}$ runs up a flight of stairs consisting of $30\text{ steps}$, each step being $15\text{ cm}$ high, in a time of $10\text{ seconds}$. Calculate:
   - a) The total vertical height climbed in meters.
   - b) The work done against gravity.
   - c) Her average power output.
"""
    }

    # Chemistry
    notes["Chemistry"] = {
        "Subatomic Particles & Configuration": r"""### 1. Atomic Structure and Theory
An **atom** is the smallest electrically neutral particle of an element that can take part in a chemical reaction. According to modern atomic theory, an atom consists of a dense central core called the **nucleus** surrounded by **electrons** that travel in pathways called energy shells.

#### Subatomic Particles:
The atom is made of three fundamental subatomic particles:

| Particle | Symbol | Relative Mass | Relative Charge | Location in Atom |
| :--- | :--- | :--- | :--- | :--- |
| **Proton** | $p$ | $1$ | $+1$ | Inside the Nucleus |
| **Neutron** | $n$ | $1$ | $0$ (Neutral) | Inside the Nucleus |
| **Electron** | $e^-$ | $\frac{1}{1840}$ (Negligible) | $-1$ | Orbiting in Energy Shells |

---

### 2. Atomic Number and Mass Number
Every element is characterized by two numbers:
1. **Atomic Number ($Z$)**: The number of protons in the nucleus of an atom. In a neutral atom, it is also equal to the number of electrons orbiting the nucleus. **It defines the identity of the element.**
2. **Mass Number ($A$)**: The total number of protons and neutrons in the nucleus of an atom.
$$\text{Mass Number (A)} = \text{Protons (Z)} + \text{Neutrons (N)}$$

#### Representation:
An element $X$ is written as:
$${}^{A}_{Z}X$$
For example, Carbon-12 is represented as ${}^{12}_{6}\text{C}$. This means it has $6$ protons, $6$ electrons, and $12 - 6 = 6$ neutrons.

---

### 3. Electronic Configuration (E.C.)
Electrons are arranged in shells (energy levels) around the nucleus, labeled $K, L, M, N...$ (where $1\text{st shell} = K$, $2\text{nd shell} = L$, etc.).

#### Shell Capacities:
- **1st Shell (K)**: Max 2 electrons.
- **2nd Shell (L)**: Max 8 electrons.
- **3rd Shell (M)**: Max 8 electrons (for the first 20 elements).

#### Rules for Filling Shells:
- Shells are filled in order of increasing energy, starting from the innermost shell.
- A shell must be fully filled before electrons enter the next outer shell.

#### Worked Electronic Configurations:
- **Sodium (Na, $Z=11$)**: $2:8:1$ (1 valence electron in the outer shell)
- **Oxygen (O, $Z=8$)**: $2:6$ (6 valence electrons)
- **Calcium (Ca, $Z=20$)**: $2:8:8:2$ (2 valence electrons)

---

### 4. Periodic Table Placement
From the electronic configuration of a neutral atom, we can determine its position in the Periodic Table:
- **Group Number** = The number of valence electrons (electrons in the outermost shell).
- **Period Number** = The number of occupied electron shells.

#### Example: Sodium ($2:8:1$)
- It has **1** valence electron, so it is in **Group I**.
- It has **3** occupied shells ($K, L, M$), so it is in **Period 3**.

---

### 5. NCDC Exam Practice Questions
1. **Question**: Complete the table below for neutral atoms:
   - a) Element $A$: Atomic number = 17, Mass number = 35. Find protons, neutrons, electrons, and E.C.
   - b) Element $B$: Protons = 12, Neutrons = 12. Find mass number, E.C., Group, and Period.
2. **Question**: State the rules governing the arrangement of electrons in the first three energy shells of an atom.
3. **Question**: Draw the Bohr atomic diagram for Carbon-12 (${}^{12}_{6}\text{C}$) showing all protons, neutrons, and electrons.
""",
        "Relative Atomic Mass & Isotopes": r"""### 1. The Concept of Isotopes
In nature, some elements exist as atoms with different mass numbers. These are called isotopes.

#### Definition:
**Isotopes** are atoms of the same element with the **same atomic number** (number of protons) but **different mass numbers** (number of neutrons).

#### Comparison of Isotopes:
- **Chemical Properties**: Isotopes have **identical** chemical properties because they have the same number of protons and electrons, and thus the same electronic configuration and number of valence electrons.
- **Physical Properties**: Isotopes have **different** physical properties (such as density, rate of diffusion, melting and boiling points) because they have different masses due to the difference in the number of neutrons.

#### Common Examples:
1. **Chlorine**:
   - Chlorine-35 (${}^{35}_{17}\text{Cl}$): $17$ protons, $17$ electrons, $18$ neutrons.
   - Chlorine-37 (${}^{37}_{17}\text{Cl}$): $17$ protons, $17$ electrons, $20$ neutrons.
2. **Hydrogen**:
   - Protium (${}^{1}_{1}\text{H}$): 1 proton, 0 neutrons.
   - Deuterium (${}^{2}_{1}\text{H}$): 1 proton, 1 neutron.
   - Tritium (${}^{3}_{1}\text{H}$): 1 proton, 2 neutrons.

---

### 2. Relative Atomic Mass ($A_r$)
The actual mass of a single atom is extremely small. Therefore, atomic masses are measured relative to a standard.

#### Definition:
The **Relative Atomic Mass ($A_r$)** of an element is the weighted average mass of one atom of the element compared to $\frac{1}{12}\text{th}$ of the mass of a Carbon-12 atom.
$$\text{Relative Atomic Mass is a ratio and has NO units.}$$

---

### 3. Calculating $A_r$ from Isotopic Abundance
The relative atomic mass of an element is calculated using the percentage abundances and mass numbers of its naturally occurring isotopes.

#### Formula:
$$A_r = \sum \left( \frac{\text{\% Abundance of Isotope } i}{100} \times \text{Mass of Isotope } i \right)$$

#### Worked Example 1: Chlorine
Naturally occurring chlorine consists of $75\%$ chlorine-35 and $25\%$ chlorine-37. Calculate the relative atomic mass of chlorine.

*Solution*:
$$A_r = \left(\frac{75}{100} \times 35\right) + \left(\frac{25}{100} \times 37\right)$$
$$A_r = 26.25 + 9.25 = 35.5$$
*Thus, the relative atomic mass of chlorine is 35.5.*

#### Worked Example 2: Algebraic Determination of Abundance
Copper has a relative atomic mass of $63.5$ and exists as two isotopes: ${}^{63}\text{Cu}$ and ${}^{65}\text{Cu}$. Find the percentage abundance of each isotope.

*Solution*:
- Let the percentage abundance of ${}^{63}\text{Cu}$ be $x\%$.
- Then, the percentage abundance of ${}^{65}\text{Cu}$ must be $(100 - x)\%$.

Set up the equation:
$$63.5 = \left(\frac{x}{100} \times 63\right) + \left(\frac{100 - x}{100} \times 65\right)$$
Multiply both sides by 100 to clear denominators:
$$6350 = 63x + 65(100 - x)$$
$$6350 = 63x + 6500 - 65x$$
$$6350 = 6500 - 2x$$
$$2x = 6500 - 6350$$
$$2x = 150 \implies x = 75$$

*Abundances: ${}^{63}\text{Cu}$ is $75\%$ and ${}^{65}\text{Cu}$ is $25\%$.*

---

### 4. NCDC Exam Practice Questions
1. **Question**: Explain why the relative atomic mass of some elements (like Chlorine, $35.5$) is not a whole number.
2. **Question**: An element $Z$ has three isotopes: ${}^{24}\text{Z}$ ($79\%$), ${}^{25}\text{Z}$ ($10\%$), and ${}^{26}\text{Z}$ ($11\%$). Calculate the relative atomic mass of $Z$ to one decimal place.
3. **Question**: Write down the differences and similarities between deuterium (${}^{2}_{1}\text{H}$) and tritium (${}^{3}_{1}\text{H}$) in terms of:
   - a) Atomic structure (subatomic particles).
   - b) Chemical behavior.
""",
        "Ionic Bonding (Dot & Cross)": r"""### 1. Introduction to Chemical Bonding
Elements (except the noble gases in Group VIII) react chemically to achieve stable electronic configurations, resembling the stable octet ($8$ electrons in the outer shell) or duplex ($2$ electrons in the K shell, e.g. Helium). They do this by gaining, losing, or sharing valence electrons.

#### Types of Bonding:
1. **Ionic (Electrovalent) Bonding**: Electron transfer from a metal to a non-metal.
2. **Covalent Bonding**: Sharing of electrons between non-metal atoms.

---

### 2. Ionic Bonding (Electrovalent)
Ionic bonding occurs between **metal atoms** (which lose electrons to form positive ions called **cations**) and **non-metal atoms** (which gain electrons to form negative ions called **anions**). The resulting oppositely charged ions are held together by strong electrostatic forces of attraction, forming an ionic compound.

---

### 3. Step-by-Step Formation and Dot-and-Cross Representation

#### A. Sodium Chloride ($NaCl$)
- Sodium ($\text{Na}$, $Z=11$) has E.C. $2:8:1$. It loses 1 valence electron to become stable:
  $$\text{Na} \rightarrow \text{Na}^+ + e^- \quad (\text{E.C. of } \text{Na}^+ \text{ is } 2:8)$$
- Chlorine ($\text{Cl}$, $Z=17$) has E.C. $2:8:7$. It gains the 1 electron lost by Sodium:
  $$\text{Cl} + e^- \rightarrow \text{Cl}^- \quad (\text{E.C. of } \text{Cl}^- \text{ is } 2:8:8)$$
- Electrostatic attraction binds $\text{Na}^+$ and $\text{Cl}^-$ to form $NaCl$.
- **Representation**:
  $$\text{Na}[\bullet] + \text{Cl}[\times\times\times\times\times\times\times] \rightarrow [\text{Na}]^+ + [\bullet\text{Cl}\times\times\times\times\times\times\times]^-$$
  *(Where $\bullet$ represents Sodium's electron, and $\times$ represents Chlorine's electrons).*

#### B. Magnesium Oxide ($MgO$)
- Magnesium ($\text{Mg}$, $Z=12$) has E.C. $2:8:2$. It loses 2 valence electrons:
  $$\text{Mg} \rightarrow \text{Mg}^{2+} + 2e^- \quad (2:8)$$
- Oxygen ($\text{O}$, $Z=8$) has E.C. $2:6$. It gains 2 electrons:
  $$\text{O} + 2e^- \rightarrow \text{O}^{2-} \quad (2:8)$$
- They combine in a $1:1$ ratio: $\text{Mg}^{2+} + \text{O}^{2-} \rightarrow MgO$.

#### C. Calcium Chloride ($CaCl_2$)
- Calcium ($\text{Ca}$, $Z=20$) has E.C. $2:8:8:2$. It loses 2 electrons.
- Chlorine ($\text{Cl}$, $Z=17$) has E.C. $2:8:7$. Each chlorine atom can only gain 1 electron.
- Therefore, one Calcium atom transfers its 2 electrons to two different Chlorine atoms:
  $$\text{Ca}^{2+} + 2\text{Cl}^- \rightarrow CaCl_2$$

---

### 4. Properties of Ionic Compounds
The physical properties of ionic compounds are explained by their **giant ionic crystal lattice** structure, where cations and anions are arranged in a regular, repeating three-dimensional pattern.

1. **High Melting and Boiling Points**: Strong electrostatic forces hold the ions together. Overcoming these forces requires a large amount of thermal energy.
2. **Electrical Conductivity**:
   - In **solid state**, they do **not** conduct electricity because the ions are locked in fixed positions in the lattice and cannot move.
   - In **molten state** or **aqueous solution (dissolved in water)**, the lattice breaks down. The ions become free to move and carry electric currents.
3. **Solubility**: Usually soluble in polar solvents like water, but insoluble in non-polar organic solvents like ether, benzene, or petrol.

---

### 5. NCDC Exam Practice Questions
1. **Question**: Draw dot-and-cross diagrams to show the bonding and formation of:
   - a) Lithium Fluoride ($LiF$) (Lithium $Z=3$, Fluorine $Z=9$)
   - b) Magnesium Chloride ($MgCl_2$) (Magnesium $Z=12$, Chlorine $Z=17$)
2. **Question**: Explain in terms of structure and bonding why sodium chloride crystals are brittle and have a melting point of $801^\circ\text{C}$.
3. **Question**: Under what conditions do ionic compounds conduct electricity? Explain your answer.
"""
    }

    # Biology
    notes["Biology"] = {
        "Aerobic vs Anaerobic Processes": r"""### 1. Understanding Respiration
Respiration is a vital biochemical process that occurs in all living cells. It involves the breakdown of organic food molecules (typically glucose) to release energy in the form of **ATP (Adenosine Triphosphate)**.

> **Respiration vs. Breathing**: Do not confuse the two! Breathing (or ventilation) is the physical process of inhaling and exhaling air. Respiration is the intracellular biochemical breakdown of glucose to release energy.

---

### 2. Aerobic Respiration
Aerobic respiration occurs in the **presence of oxygen**. It involves the complete oxidation of glucose into carbon dioxide and water, releasing a large amount of energy.

- **Chemical Equation**:
  $$\text{Glucose} + \text{Oxygen} \rightarrow \text{Carbon Dioxide} + \text{Water} + \text{Energy (ATP)}$$
  $$\text{C}_6\text{H}_{12}\text{O}_6 + 6\text{O}_2 \rightarrow 6\text{CO}_2 + 6\text{H}_2\text{O} + 38\text{ ATP} \quad (2880\text{ kJ})$$
- **Site of Reaction**: Initiated in the cytoplasm (glycolysis) and completed in the **mitochondria** (Krebs cycle and Electron Transport Chain).

---

### 3. Anaerobic Respiration
Anaerobic respiration occurs in the **absence of oxygen**. It involves the partial breakdown of glucose, resulting in a much lower energy yield.

#### A. In Plants and Yeast (Alcoholic Fermentation):
Yeast cells break down glucose into ethanol (alcohol) and carbon dioxide.
- **Chemical Equation**:
  $$\text{Glucose} \rightarrow \text{Ethanol} + \text{Carbon Dioxide} + \text{Energy (ATP)}$$
  $$\text{C}_6\text{H}_{12}\text{O}_6 \rightarrow 2\text{C}_2\text{H}_5\text{OH} + 2\text{CO}_2 + 2\text{ ATP} \quad (150\text{ kJ})$$
- **Commercial Applications**:
  - **Baking**: The carbon dioxide gas produced bubbles, causing bread dough to rise.
  - **Brewing**: Ethanol is the alcohol found in beers, wines, and spirits.

#### B. In Animal Muscle Cells:
During strenuous exercise (e.g., sprinting), the oxygen demand of muscles exceeds the oxygen supply. Muscle cells switch to anaerobic respiration to produce extra energy, creating lactic acid.
- **Chemical Equation**:
  $$\text{Glucose} \rightarrow \text{Lactic Acid} + \text{Energy (ATP)}$$
  $$\text{C}_6\text{H}_{12}\text{O}_6 \rightarrow 2\text{C}_3\text{H}_6\text{O}_3 + 2\text{ ATP} \quad (120\text{ kJ})$$
- **Muscle Fatigue and Oxygen Debt**:
  - **Lactic Acid Accumulation**: Causes muscle cramps, pain, and fatigue.
  - **Oxygen Debt**: The temporary shortage of oxygen in body tissues. After exercise, deep and rapid breathing continues to supply oxygen to the liver, where lactic acid is oxidized into water and carbon dioxide or converted back to glycogen. This is called *repaying the oxygen debt*.

---

### 4. Comparison Summary Table

| Feature | Aerobic Respiration | Anaerobic Respiration |
| :--- | :--- | :--- |
| **Oxygen requirement** | Required | Not required |
| **Breakdown of Glucose** | Complete | Partial |
| **End products** | Carbon dioxide and water | Animals: Lactic acid. Yeast: Ethanol and $CO_2$ |
| **Energy yield per glucose**| Very high ($38\text{ ATP}$ / $2880\text{ kJ}$) | Low ($2\text{ ATP}$ / $120\text{-}150\text{ kJ}$) |
| **Site inside the cell** | Cytoplasm and Mitochondria | Cytoplasm only |

---

### 5. NCDC Exam Practice Questions
1. **Question**: State three differences between aerobic and anaerobic respiration.
2. **Question**: Write word and balanced chemical equations for anaerobic respiration in:
   - a) Yeast cells.
   - b) Active muscle cells.
3. **Question**: Explain what is meant by *oxygen debt* and how it is repaid after a sprint race.
""",
        "Human Breathing & Ventilation": r"""### 1. Anatomy of the Human Respiratory System
Before studying how we breathe, we must understand the respiratory pathway.

#### Air Pathway:
$$\text{Nostrils} \rightarrow \text{Nasal Cavity} \rightarrow \text{Pharynx} \rightarrow \text{Larynx} \rightarrow \text{Trachea} \rightarrow \text{Bronchi} \rightarrow \text{Bronchioles} \rightarrow \text{Alveoli}$$

#### Specialized Structures:
- **Cartilage Rings**: The trachea is lined with C-shaped rings of cartilage that prevent it from collapsing when pressure drops during inhalation.
- **Ciliated Epithelium**: The trachea and bronchi are lined with hair-like cilia and goblet cells. Goblet cells produce **mucus** to trap dust and pathogens, while cilia sweep the mucus upwards to the pharynx to be swallowed or coughed out.
- **Pleural Membranes and Fluid**: Lungs are surrounded by double-layered pleural membranes. The pleural cavity between them contains pleural fluid, which acts as a lubricant to reduce friction between the lungs and the chest wall during breathing.

---

### 2. Mechanics of Ventilation (Breathing)
Breathing is a mechanical process of moving air in and out of the lungs. It depends on altering the volume of the thoracic cavity to create pressure gradients.

```
       INHALATION                             EXHALATION
     ==============                         ==============
  Ribcage moves Up & Out                 Ribcage moves Down & In
  Diaphragm Flattens (contracts)         Diaphragm Domes (relaxes)
  Volume Increases                       Volume Decreases
  Pressure Drops                         Pressure Rises
  Air enters Lungs                       Air exits Lungs
```

#### A. Inhalation (Inspiration) - Breathing In:
1. The **external intercostal muscles contract**, causing the rib cage to move **upward and outward**.
2. The **diaphragm muscles contract**, pulling the diaphragm **downward and flattening it**.
3. These movements **increase the volume** of the thoracic cavity.
4. The increase in volume causes the **air pressure inside the lungs to decrease** below atmospheric pressure.
5. Air rushes from the higher atmospheric pressure outside, through the nasal passages, into the lungs.

#### B. Exhalation (Expiration) - Breathing Out:
1. The **external intercostal muscles relax**, causing the rib cage to move **downward and inward** under its own weight.
2. The **diaphragm muscles relax**, rising back to its resting **dome shape**.
3. These movements **decrease the volume** of the thoracic cavity.
4. The decrease in volume **increases the air pressure inside the lungs** above atmospheric pressure.
5. Air is forced out of the lungs into the atmosphere.

---

### 3. The Bell Jar Model of Ventilation
The bell jar is a classic laboratory model used to demonstrate the mechanics of breathing.

- **Bell Jar** = Rib cage / Chest wall
- **Y-shaped tube** = Trachea and Bronchi
- **Balloons** = Lungs
- **Rubber Sheet** = Diaphragm
- **Space inside Jar** = Thoracic Cavity

#### Limitations of the Model:
- The glass jar is rigid and cannot move up, down, out, or in like the real rib cage.
- The model lacks intercostal muscles.
- The volume changes in the jar are solely caused by the rubber sheet (diaphragm).

---

### 4. NCDC Exam Practice Questions
1. **Question**: Describe the steps involved in the process of exhalation in humans.
2. **Question**: State the function of:
   - a) C-shaped cartilage rings in the trachea.
   - b) Pleural fluid.
   - c) Ciliated cells.
3. **Question**: In the bell jar model, pulling the rubber sheet downwards causes the balloons to inflate. Explain this observation using pressure and volume terms.
""",
        "Alveolar Diffusion Adaptations": r"""### 1. Gaseous Exchange in the Alveoli
Gaseous exchange occurs in the **alveoli** (air sacs) of the lungs. It is the physical process by which oxygen enters the blood and carbon dioxide leaves the blood. This exchange happens entirely by **simple diffusion**.

- **Oxygen**: High concentration in alveoli $\rightarrow$ diffuses into deoxygenated blood in capillaries (binds to hemoglobin to form **oxyhemoglobin**).
- **Carbon Dioxide**: High concentration in blood capillaries $\rightarrow$ diffuses into the alveolar air space to be exhaled.

---

### 2. Adaptations of the Alveoli for Gaseous Exchange
To maximize the rate of diffusion, the alveoli have specific structural adaptations:

1. **Very Thin Respiratory Membrane**: The alveolar wall is only one cell thick (made of thin squamous epithelium), and the capillary wall is also one cell thick. This makes the diffusion distance extremely short.
2. **Large Surface Area**: Lungs contain millions of alveoli. The combined surface area is approximately $70\text{ m}^2$ (roughly the size of a tennis court), providing a massive area for gas exchange.
3. **Moist Alveolar Lining**: A thin layer of moisture coats the inner surface of the alveolus. Oxygen dissolves in this liquid before diffusing across the cells.
4. **Rich Capillary Network**: The alveoli are surrounded by a dense network of blood capillaries. The constant flow of blood rapidly removes oxygen and brings carbon dioxide, maintaining a steep concentration gradient.

---

### 3. Effects of Cigarette Smoking on the Lungs
Tobacco smoke contains thousands of chemicals, three of which are highly toxic to the respiratory system:

#### A. Tar:
- Destroys the cilia in the respiratory tract.
- Causes cells to secrete excess mucus, which cannot be swept away. This blocks airways and leads to **smoker's cough** and **chronic bronchitis**.
- Contains carcinogens that can cause **lung cancer**.

#### B. Nicotine:
- An addictive drug that stimulates the nervous system.
- Causes blood vessels to narrow, increasing blood pressure and the risk of coronary heart disease.

#### C. Carbon Monoxide ($CO$):
- A poisonous gas that binds irreversibly to hemoglobin, forming **carboxyhemoglobin**.
- This reduces the blood's capacity to transport oxygen around the body, forcing the heart to work harder.

#### D. Emphysema:
- Constant coughing and irritation break down the thin walls separating individual alveoli.
- This merges tiny air sacs into larger, irregular spaces, drastically reducing the surface area available for gaseous exchange.
- Patients suffer from severe breathlessness and fatigue.

---

### 4. NCDC Exam Practice Questions
1. **Question**: List four structural adaptations of the alveolus that facilitate rapid gaseous exchange.
2. **Question**: Explain how cigarette smoking causes emphysema and how this affects a person's athletic performance.
3. **Question**: Compare the composition of inhaled and exhaled air in terms of:
   - a) Oxygen percentage.
   - b) Carbon dioxide percentage.
   - c) Water vapor content.
"""
    }

    sub_notes = notes.get(subject, {})
    return sub_notes.get(lesson, None)


def get_s2_detailed_questions(subject, lesson):
    questions = {}
    
    # Mathematics
    questions["Mathematics"] = {
        "Solving Linear Equations": [
            {
                "text": r"Solve for $x$: $3x - 7 = 14$",
                "choices": [
                    {"text": r"$x = 7$", "is_correct": True},
                    {"text": r"$x = 3$", "is_correct": False},
                    {"text": r"$x = 21$", "is_correct": False},
                    {"text": r"$x = -7$", "is_correct": False}
                ]
            },
            {
                "text": r"Solve for $y$: $5(y - 3) = 2y + 9$",
                "choices": [
                    {"text": r"$y = 8$", "is_correct": True},
                    {"text": r"$y = 2$", "is_correct": False},
                    {"text": r"$y = 12$", "is_correct": False},
                    {"text": r"$y = -8$", "is_correct": False}
                ]
            },
            {
                "text": r"If $\frac{2w - 3}{5} = 3$, what is the value of $w$?",
                "choices": [
                    {"text": r"$w = 9$", "is_correct": True},
                    {"text": r"$w = 6$", "is_correct": False},
                    {"text": r"$w = 7.5$", "is_correct": False},
                    {"text": r"$w = 18$", "is_correct": False}
                ]
            }
        ],
        "Elimination & Substitution Methods": [
            {
                "text": r"What is the solution to the simultaneous equations: $2x + 3y = 12$ and $x - y = 1$?",
                "choices": [
                    {"text": r"$x = 3, y = 2$", "is_correct": True},
                    {"text": r"$x = 2, y = 3$", "is_correct": False},
                    {"text": r"$x = 1, y = 0$", "is_correct": False},
                    {"text": r"$x = 4, y = 1$", "is_correct": False}
                ]
            },
            {
                "text": r"Solve the system: $3x + 2y = 16$ and $2x - y = 6$.",
                "choices": [
                    {"text": r"$x = 4, y = 2$", "is_correct": True},
                    {"text": r"$x = 2, y = 5$", "is_correct": False},
                    {"text": r"$x = 5, y = 4$", "is_correct": False},
                    {"text": r"$x = 3, y = 3$", "is_correct": False}
                ]
            },
            {
                "text": r"A farmer has chickens (2 legs) and goats (4 legs). The total number of animals is 35, and the total number of legs is 110. How many goats does the farmer have?",
                "choices": [
                    {"text": r"$20$", "is_correct": True},
                    {"text": r"$15$", "is_correct": False},
                    {"text": r"$10$", "is_correct": False},
                    {"text": r"$25$", "is_correct": False}
                ]
            }
        ],
        "Angle Properties of Circles": [
            {
                "text": r"If chord $CD$ subtends an angle $CAD = 48^\circ$ at the circumference, what is the angle $CBD$ subtended by the same chord at another point on the major arc?",
                "choices": [
                    {"text": r"$48^\circ$", "is_correct": True},
                    {"text": r"$96^\circ$", "is_correct": False},
                    {"text": r"$24^\circ$", "is_correct": False},
                    {"text": r"$132^\circ$", "is_correct": False}
                ]
            },
            {
                "text": r"An arc $AB$ subtends an angle of $130^\circ$ at the center $O$. Calculate the angle subtended by $AB$ at the circumference point $P$.",
                "choices": [
                    {"text": r"$65^\circ$", "is_correct": True},
                    {"text": r"$260^\circ$", "is_correct": False},
                    {"text": r"$130^\circ$", "is_correct": False},
                    {"text": r"$50^\circ$", "is_correct": False}
                ]
            },
            {
                "text": r"What is the angle subtended by a diameter at any point on the circumference of a circle?",
                "choices": [
                    {"text": r"$90^\circ$", "is_correct": True},
                    {"text": r"$180^\circ$", "is_correct": False},
                    {"text": r"$45^\circ$", "is_correct": False},
                    {"text": r"Depends on the circle's radius", "is_correct": False}
                ]
            }
        ]
    }

    # Physics
    questions["Physics"] = {
        "Inertia & Newton's First Law": [
            {
                "text": r"Which of the following physical quantities is a direct measure of a body's inertia?",
                "choices": [
                    {"text": r"Mass", "is_correct": True},
                    {"text": r"Weight", "is_correct": False},
                    {"text": r"Velocity", "is_correct": False},
                    {"text": r"Acceleration", "is_correct": False}
                ]
            },
            {
                "text": r"When a moving bus brakes suddenly, passengers are thrown forward. This is because:",
                "choices": [
                    {"text": r"Their upper bodies continue moving forward due to inertia.", "is_correct": True},
                    {"text": r"The force of friction pushes them forward.", "is_correct": False},
                    {"text": r"Gravity pulls them forward.", "is_correct": False},
                    {"text": r"The bus applies a forward force on them.", "is_correct": False}
                ]
            },
            {
                "text": r"Newton's First Law of Motion is also widely referred to as the:",
                "choices": [
                    {"text": r"Law of Inertia", "is_correct": True},
                    {"text": r"Law of Momentum", "is_correct": False},
                    {"text": r"Law of Action and Reaction", "is_correct": False},
                    {"text": r"Law of Gravitation", "is_correct": False}
                ]
            }
        ],
        "Force & Newton's Second Law ($F = ma$)": [
            {
                "text": r"A force of $20\text{ N}$ acts on a mass of $4\text{ kg}$. Find the acceleration of the mass.",
                "choices": [
                    {"text": r"$5\text{ m/s}^2$", "is_correct": True},
                    {"text": r"$80\text{ m/s}^2$", "is_correct": False},
                    {"text": r"$0.2\text{ m/s}^2$", "is_correct": False},
                    {"text": r"$24\text{ m/s}^2$", "is_correct": False}
                ]
            },
            {
                "text": r"What is the SI unit of linear momentum?",
                "choices": [
                    {"text": r"$\text{kg}\cdot\text{m/s}$", "is_correct": True},
                    {"text": r"$\text{kg}\cdot\text{m/s}^2$", "is_correct": False},
                    {"text": r"$\text{N}\cdot\text{m}$", "is_correct": False},
                    {"text": r"$\text{Joules}$", "is_correct": False}
                ]
            },
            {
                "text": r"If a $1500\text{ kg}$ car accelerates from rest to $20\text{ m/s}$ in $5\text{ seconds}$, calculate the net force acting on it.",
                "choices": [
                    {"text": r"$6000\text{ N}$", "is_correct": True},
                    {"text": r"$300\text{ N}$", "is_correct": False},
                    {"text": r"$7500\text{ N}$", "is_correct": False},
                    {"text": r"$1500\text{ N}$", "is_correct": False}
                ]
            }
        ],
        "Action & Reaction (Third Law)": [
            {
                "text": r"Which of the following is true about Newton's Third Law action-reaction force pairs?",
                "choices": [
                    {"text": r"They act on different bodies and therefore do not cancel each other out.", "is_correct": True},
                    {"text": r"They act on the same body and cancel each other out.", "is_correct": False},
                    {"text": r"Action is always greater than reaction.", "is_correct": False},
                    {"text": r"They only occur when objects are in motion.", "is_correct": False}
                ]
            },
            {
                "text": r"A rifle recoils when a bullet is fired. This is because:",
                "choices": [
                    {"text": r"The bullet exerts an equal and opposite backward force on the rifle.", "is_correct": True},
                    {"text": r"The gunpowder explosion pushes the rifle back only.", "is_correct": False},
                    {"text": r"Gravity pulls the rifle down.", "is_correct": False},
                    {"text": r"Air resistance pushes the rifle back.", "is_correct": False}
                ]
            },
            {
                "text": r"When walking, the reaction force that moves you forward is exerted by:",
                "choices": [
                    {"text": r"The ground on your foot.", "is_correct": True},
                    {"text": r"Your foot on the ground.", "is_correct": False},
                    {"text": r"Your muscles on your bones.", "is_correct": False},
                    {"text": r"Gravity on your body.", "is_correct": False}
                ]
            }
        ],
        "Work Done & Calculations": [
            {
                "text": r"A student lifts a box of books weighing $50\text{ N}$ through a vertical height of $1.5\text{ m}$. Calculate the work done.",
                "choices": [
                    {"text": r"$75\text{ J}$", "is_correct": True},
                    {"text": r"$33.3\text{ J}$", "is_correct": False},
                    {"text": r"$7.5\text{ J}$", "is_correct": False},
                    {"text": r"$0\text{ J}$", "is_correct": False}
                ]
            },
            {
                "text": r"In which of the following cases is the work done scientifically ZERO?",
                "choices": [
                    {"text": r"A man carrying a heavy load on his head while walking horizontally.", "is_correct": True},
                    {"text": r"An apple falling from a tree to the ground.", "is_correct": False},
                    {"text": r"A crane lifting a container vertically upwards.", "is_correct": False},
                    {"text": r"A student pushing a trolley across a room.", "is_correct": False}
                ]
            },
            {
                "text": r"An engine does $6000\text{ J}$ of work in $2\text{ minutes}$. What is the power output of the engine?",
                "choices": [
                    {"text": r"$50\text{ W}$", "is_correct": True},
                    {"text": r"$3000\text{ W}$", "is_correct": False},
                    {"text": r"$12000\text{ W}$", "is_correct": False},
                    {"text": r"$100\text{ W}$", "is_correct": False}
                ]
            }
        ]
    }

    # Chemistry
    questions["Chemistry"] = {
        "Subatomic Particles & Configuration": [
            {
                "text": r"Which subatomic particle has a relative mass of $1/1840$ and a relative charge of $-1$?",
                "choices": [
                    {"text": r"Electron", "is_correct": True},
                    {"text": r"Proton", "is_correct": False},
                    {"text": r"Neutron", "is_correct": False},
                    {"text": r"Alpha particle", "is_correct": False}
                ]
            },
            {
                "text": r"What is the electronic configuration of Sodium (Atomic number 11)?",
                "choices": [
                    {"text": r"$2:8:1$", "is_correct": True},
                    {"text": r"$2:9$", "is_correct": False},
                    {"text": r"$2:8:2$", "is_correct": False},
                    {"text": r"$1:8:2$", "is_correct": False}
                ]
            },
            {
                "text": r"An element has atomic number 16. In which Group and Period of the Periodic Table is it located?",
                "choices": [
                    {"text": r"Group VI, Period 3", "is_correct": True},
                    {"text": r"Group III, Period 6", "is_correct": False},
                    {"text": r"Group IV, Period 4", "is_correct": False},
                    {"text": r"Group VIII, Period 2", "is_correct": False}
                ]
            }
        ],
        "Relative Atomic Mass & Isotopes": [
            {
                "text": r"Isotopes are atoms of the same element with:",
                "choices": [
                    {"text": r"Same atomic number but different mass numbers.", "is_correct": True},
                    {"text": r"Same mass number but different atomic numbers.", "is_correct": False},
                    {"text": r"Different number of protons and electrons.", "is_correct": False},
                    {"text": r"Different chemical properties.", "is_correct": False}
                ]
            },
            {
                "text": r"Chlorine exists as $75\%$ Chlorine-35 and $25\%$ Chlorine-37. What is its Relative Atomic Mass?",
                "choices": [
                    {"text": r"$35.5$", "is_correct": True},
                    {"text": r"$36.0$", "is_correct": False},
                    {"text": r"$35.0$", "is_correct": False},
                    {"text": r"$37.0$", "is_correct": False}
                ]
            },
            {
                "text": r"Why do isotopes of the same element have identical chemical properties?",
                "choices": [
                    {"text": r"They have the same number of valence electrons.", "is_correct": True},
                    {"text": r"They have the same number of neutrons.", "is_correct": False},
                    {"text": r"They have the same atomic mass.", "is_correct": False},
                    {"text": r"They are found in the same location in nature.", "is_correct": False}
                ]
            }
        ],
        "Ionic Bonding (Dot & Cross)": [
            {
                "text": r"Ionic bonding typically occurs between:",
                "choices": [
                    {"text": r"Metals and non-metals by transfer of electrons.", "is_correct": True},
                    {"text": r"Non-metals and non-metals by sharing of electrons.", "is_correct": False},
                    {"text": r"Metals and metals by sharing of electrons.", "is_correct": False},
                    {"text": r"Noble gases and transition metals.", "is_correct": False}
                ]
            },
            {
                "text": r"Which of the following is a characteristic property of ionic compounds?",
                "choices": [
                    {"text": r"High melting point and electrical conductivity in molten/aqueous state.", "is_correct": True},
                    {"text": r"Low melting point and solubility in organic solvents.", "is_correct": False},
                    {"text": r"Electrical conductivity in solid state.", "is_correct": False},
                    {"text": r"Composed of neutral molecules.", "is_correct": False}
                ]
            },
            {
                "text": r"During the formation of Magnesium Oxide ($MgO$), how many electrons are transferred from a Magnesium atom to an Oxygen atom?",
                "choices": [
                    {"text": r"$2$", "is_correct": True},
                    {"text": r"$1$", "is_correct": False},
                    {"text": r"$3$", "is_correct": False},
                    {"text": r"$4$", "is_correct": False}
                ]
            }
        ]
    }

    # Biology
    questions["Biology"] = {
        "Aerobic vs Anaerobic Processes": [
            {
                "text": r"What are the end products of anaerobic respiration in yeast cells (alcoholic fermentation)?",
                "choices": [
                    {"text": r"Ethanol, carbon dioxide, and 2 ATP", "is_correct": True},
                    {"text": r"Lactic acid and 2 ATP", "is_correct": False},
                    {"text": r"Carbon dioxide, water, and 38 ATP", "is_correct": False},
                    {"text": r"Glucose and oxygen", "is_correct": False}
                ]
            },
            {
                "text": r"Why is the energy yield in anaerobic respiration much lower than in aerobic respiration?",
                "choices": [
                    {"text": r"Glucose is only partially broken down, leaving energy stored in ethanol/lactic acid.", "is_correct": True},
                    {"text": r"Oxygen is present to destroy the energy molecules.", "is_correct": False},
                    {"text": r"Yeast cells do not have mitochondria to make ATP.", "is_correct": False},
                    {"text": r"Carbon dioxide absorbs the energy.", "is_correct": False}
                ]
            },
            {
                "text": r"The biochemical site where most aerobic respiration reactions take place is the:",
                "choices": [
                    {"text": r"Mitochondria", "is_correct": True},
                    {"text": r"Chloroplast", "is_correct": False},
                    {"text": r"Cytoplasm", "is_correct": False},
                    {"text": r"Ribosome", "is_correct": False}
                ]
            }
        ],
        "Human Breathing & Ventilation": [
            {
                "text": r"During inhalation (inspiration) in humans, what happens to the diaphragm and external intercostal muscles?",
                "choices": [
                    {"text": r"Diaphragm contracts (flattens) and external intercostal muscles contract (ribs move up and out).", "is_correct": True},
                    {"text": r"Diaphragm relaxes (domes) and external intercostal muscles relax.", "is_correct": False},
                    {"text": r"Diaphragm contracts and external intercostal muscles relax.", "is_correct": False},
                    {"text": r"Diaphragm relaxes and external intercostal muscles contract.", "is_correct": False}
                ]
            },
            {
                "text": r"What is the main function of the C-shaped cartilage rings in the trachea?",
                "choices": [
                    {"text": r"To keep the trachea open and prevent it from collapsing during pressure changes.", "is_correct": True},
                    {"text": r"To produce mucus to trap dust particles.", "is_correct": False},
                    {"text": r"To help in the production of voice/sound.", "is_correct": False},
                    {"text": r"To absorb oxygen from the inhaled air.", "is_correct": False}
                ]
            },
            {
                "text": r"During exhalation, the pressure inside the lungs:",
                "choices": [
                    {"text": r"Increases above atmospheric pressure, forcing air out.", "is_correct": True},
                    {"text": r"Decreases below atmospheric pressure, drawing air in.", "is_correct": False},
                    {"text": r"Remains exactly equal to atmospheric pressure.", "is_correct": False},
                    {"text": r"Drops to zero.", "is_correct": False}
                ]
            }
        ],
        "Alveolar Diffusion Adaptations": [
            {
                "text": r"Which of the following is NOT an adaptation of the alveoli for efficient gas exchange?",
                "choices": [
                    {"text": r"Thick muscular walls to pump gases into capillaries.", "is_correct": True},
                    {"text": r"Single-cell thick walls of alveoli and capillaries.", "is_correct": False},
                    {"text": r"A moist surface lining to dissolve gases.", "is_correct": False},
                    {"text": r"A large surface area provided by millions of alveoli.", "is_correct": False}
                ]
            },
            {
                "text": r"Smoking cigarettes causes a disease where alveolar walls break down, reducing surface area for gas exchange. This is called:",
                "choices": [
                    {"text": r"Emphysema", "is_correct": True},
                    {"text": r"Asthma", "is_correct": False},
                    {"text": r"Bronchitis", "is_correct": False},
                    {"text": r"Tuberculosis", "is_correct": False}
                ]
            },
            {
                "text": r"How is carbon dioxide primarily transported in human blood?",
                "choices": [
                    {"text": r"As hydrogen carbonate (bicarbonate) ions in blood plasma.", "is_correct": True},
                    {"text": r"Bound to hemoglobin as carbaminohemoglobin.", "is_correct": False},
                    {"text": r"As carbon monoxide gas.", "is_correct": False},
                    {"text": r"As bubbles dissolved in red blood cells.", "is_correct": False}
                ]
            }
        ]
    }

    sub_questions = questions.get(subject, {})
    return sub_questions.get(lesson, [])


def get_ugandan_curriculum(level_name, subject_name):
    is_primary = level_name.startswith('P.')
    is_olevel = level_name in ['S.1', 'S.2', 'S.3', 'S.4']
    is_alevel = level_name in ['S.5', 'S.6']
    
    try:
        level_num = int(level_name[2:])
    except:
        level_num = 1
        
    if is_primary:
        if "Mathematics" in subject_name:
            if level_num <= 3:
                return [
                    { "title": "Sorting and Matching", "lessons": [("Sorting Objects", "Practice", 20)] },
                    { "title": "Counting 1-100", "lessons": [("Number Sequences", "Video Lesson", 15)] },
                    { "title": "Simple Addition & Subtraction", "lessons": [("Adding Objects", "Interactive Quiz", 20)] }
                ]
            elif level_num <= 5:
                return [
                    { "title": "Sets", "lessons": [("Forming Sets", "Video Lesson", 20)] },
                    { "title": "Whole Numbers", "lessons": [("Place Values", "Practice", 25), ("Multiplication Tables", "Interactive Quiz", 20)] },
                    { "title": "Fractions", "lessons": [("Proper Fractions", "Video Lesson", 20)] },
                    { "title": "Geometry", "lessons": [("Shapes and Angles", "Practice", 15)] }
                ]
            else:
                return [
                    { "title": "Sets and Venn Diagrams", "lessons": [("Intersection and Union", "Video Lesson", 25)] },
                    { "title": "Operations on Whole Numbers", "lessons": [("BODMAS", "Practice", 30)] },
                    { "title": "Decimals and Percentages", "lessons": [("Conversions", "Interactive Quiz", 20)] },
                    { "title": "Integers", "lessons": [("Number Lines", "Video Lesson", 20)] },
                    { "title": "Geometry", "lessons": [("Properties of Polygons", "Practice", 25)] }
                ]
        elif "English" in subject_name:
            if level_num <= 3:
                return [
                    { "title": "Phonics", "lessons": [("Letter Sounds", "Video Lesson", 15)] },
                    { "title": "Vocabulary", "lessons": [("Things in the Classroom", "Interactive Quiz", 20)] },
                    { "title": "Handwriting", "lessons": [("Forming Letters", "Practice", 15)] }
                ]
            else:
                return [
                    { "title": "Grammar", "lessons": [("Tenses", "Video Lesson", 20), ("Parts of Speech", "Practice", 25)] },
                    { "title": "Comprehension", "lessons": [("Reading Passages", "Reading Material", 30)] },
                    { "title": "Composition", "lessons": [("Writing Letters", "Practice", 35)] }
                ]
        elif "Science" in subject_name:
            if level_num <= 3:
                return [
                    { "title": "Personal Hygiene", "lessons": [("Cleaning the Body", "Video Lesson", 15)] },
                    { "title": "Our Environment", "lessons": [("Things Around Us", "Interactive Quiz", 20)] },
                    { "title": "Plants and Animals", "lessons": [("Domestic Animals", "Video Lesson", 20)] }
                ]
            else:
                return [
                    { "title": "Human Body Systems", "lessons": [("The Digestive System", "Video Lesson", 25), ("The Respiratory System", "Reading Material", 20)] },
                    { "title": "Matter and Energy", "lessons": [("States of Matter", "Simulation", 20)] },
                    { "title": "Sanitation", "lessons": [("Keeping the Community Clean", "Practice", 15)] },
                    { "title": "Immunization", "lessons": [("Childhood Diseases", "Reading Material", 20)] }
                ]
        elif "Studies" in subject_name or "SST" in subject_name:
            if level_num <= 3:
                return [
                    { "title": "Our School", "lessons": [("People in our School", "Video Lesson", 15)] },
                    { "title": "Our Home", "lessons": [("Roles of Family Members", "Interactive Quiz", 15)] },
                    { "title": "Our Neighborhood", "lessons": [("Important Places", "Practice", 20)] }
                ]
            elif level_num == 4:
                return [
                    { "title": "Location of our District", "lessons": [("Using a Map", "Practice", 25)] },
                    { "title": "Leaders in our District", "lessons": [("Local Councils", "Reading Material", 20)] }
                ]
            elif level_num == 5:
                return [
                    { "title": "Physical Features of Uganda", "lessons": [("Mountains and Lakes", "Video Lesson", 30)] },
                    { "title": "History of Uganda", "lessons": [("Pre-colonial Societies", "Reading Material", 25)] }
                ]
            else:
                return [
                    { "title": "Physical Features of East Africa", "lessons": [("The Rift Valley", "Video Lesson", 25)] },
                    { "title": "The People of East Africa", "lessons": [("Ethnic Groups", "Reading Material", 20)] },
                    { "title": "Independence Movements", "lessons": [("Struggle for Freedom", "Video Lesson", 30)] }
                ]
        elif "Religious" in subject_name:
            return [
                { "title": "God's Creation", "lessons": [("The Story of Creation", "Reading Material", 20)] },
                { "title": "Living in Peace", "lessons": [("Forgiveness", "Story", 15)] }
            ]

    elif is_olevel:
        if "Mathematics" in subject_name:
            if level_num == 1:
                return [
                    { "title": "Natural Numbers", "lessons": [("Factors and Multiples", "Practice", 30)] },
                    { "title": "Fractions & Decimals", "lessons": [("Operations on Fractions", "Video Lesson", 25)] },
                    { "title": "Algebraic Expressions", "lessons": [("Simplifying Expressions", "Interactive Quiz", 20)] }
                ]
            elif level_num == 2:
                return [
                    { "title": "Linear & Simultaneous Equations", "lessons": [("Solving Linear Equations", "Reading Material", 30), ("Elimination & Substitution Methods", "Reading Material", 40)] },
                    { "title": "Circle Geometry & Theorems", "lessons": [("Angle Properties of Circles", "Reading Material", 25)] }
                ]
            elif level_num == 4:
                return [
                    { "title": "Matrices", "lessons": [("Matrix Multiplication", "Practice", 35)] },
                    { "title": "Trigonometry", "lessons": [("Sine & Cosine Rules", "Video Lesson", 30)] },
                    { "title": "Vectors", "lessons": [("Addition of Vectors", "Interactive Quiz", 25)] },
                    { "title": "Statistics", "lessons": [("Histograms and Ogives", "Simulation", 40)] }
                ]
            else:
                return [
                    { "title": "Sets", "lessons": [("Venn Diagrams", "Video Lesson", 30)] },
                    { "title": "Simultaneous Equations", "lessons": [("Substitution and Elimination", "Practice", 40)] },
                    { "title": "Geometry", "lessons": [("Circle Properties", "Interactive Quiz", 25)] }
                ]
        elif "Physics" in subject_name:
            if level_num == 1:
                return [
                    { "title": "Measurements", "lessons": [("SI Units", "Reading Material", 20), ("Measuring Instruments", "Simulation", 25)] },
                    { "title": "Matter", "lessons": [("States of Matter", "Video Lesson", 20)] }
                ]
            elif level_num == 2:
                return [
                    { "title": "Force & Newton's Laws", "lessons": [("Inertia & Newton's First Law", "Reading Material", 30), ("Force & Newton's Second Law ($F = ma$)", "Reading Material", 35), ("Action & Reaction (Third Law)", "Reading Material", 25)] },
                    { "title": "Work, Energy & Power", "lessons": [("Work Done & Calculations", "Reading Material", 30)] }
                ]
            elif level_num == 4:
                return [
                    { "title": "Electricity", "lessons": [("Ohm's Law", "Simulation", 30)] },
                    { "title": "Magnetism", "lessons": [("Electromagnetic Induction", "Video Lesson", 35)] },
                    { "title": "Modern Physics", "lessons": [("Cathode Rays", "Reading Material", 20)] }
                ]
            else:
                return [
                    { "title": "Mechanics", "lessons": [("Newton's Laws", "Video Lesson", 30)] },
                    { "title": "Heat", "lessons": [("Specific Heat Capacity", "Practice", 25)] },
                    { "title": "Optics", "lessons": [("Lenses", "Simulation", 30)] }
                ]
        elif "Chemistry" in subject_name:
            if level_num == 1:
                return [
                    { "title": "Introduction to Chemistry", "lessons": [("Laboratory Apparatus", "Simulation", 20)] },
                    { "title": "Mixtures", "lessons": [("Separation Techniques", "Video Lesson", 25)] }
                ]
            elif level_num == 2:
                return [
                    { "title": "Atomic Structure & Periodicity", "lessons": [("Subatomic Particles & Configuration", "Reading Material", 25), ("Relative Atomic Mass & Isotopes", "Reading Material", 20)] },
                    { "title": "Chemical Bonding", "lessons": [("Ionic Bonding (Dot & Cross)", "Reading Material", 30)] }
                ]
            else:
                return [
                    { "title": "Atomic Structure", "lessons": [("Isotopes", "Reading Material", 20)] },
                    { "title": "Acids and Bases", "lessons": [("Titration", "Simulation", 30)] },
                    { "title": "Carbon Chemistry", "lessons": [("Hydrocarbons", "Video Lesson", 25)] }
                ]
        elif "Biology" in subject_name:
            if level_num == 2:
                return [
                    { "title": "Respiration & Energy", "lessons": [("Aerobic vs Anaerobic Processes", "Reading Material", 25)] },
                    { "title": "Gas Exchange Systems", "lessons": [("Human Breathing & Ventilation", "Reading Material", 30), ("Alveolar Diffusion Adaptations", "Reading Material", 25)] }
                ]
            else:
                return [
                    { "title": "Cell Biology", "lessons": [("Plant and Animal Cells", "Video Lesson", 20)] },
                    { "title": "Nutrition", "lessons": [("Photosynthesis", "Simulation", 25), ("Human Digestive System", "Interactive Quiz", 20)] },
                    { "title": "Ecology", "lessons": [("Food Chains", "Reading Material", 15)] }
                ]
        elif "English" in subject_name:
            return [
                { "title": "Summary Writing", "lessons": [("Identifying Main Points", "Practice", 25)] },
                { "title": "Letter Writing", "lessons": [("Formal Letters", "Practice", 30)] },
                { "title": "Comprehension", "lessons": [("Analyzing Texts", "Video Lesson", 25)] },
                { "title": "Essay Writing", "lessons": [("Descriptive Essays", "Practice", 35)] }
            ]
        elif "Geography" in subject_name:
            return [
                { "title": "Map Reading", "lessons": [("Grid References", "Practice", 30)] },
                { "title": "Physical Geography", "lessons": [("Internal Land-forming Processes", "Video Lesson", 35)] }
            ]
        elif "History" in subject_name:
            return [
                { "title": "Pre-colonial Era", "lessons": [("Migration of the Bantu", "Video Lesson", 30)] },
                { "title": "Colonial Rule", "lessons": [("Indirect Rule", "Reading Material", 25)] }
            ]
        elif "Technology" in subject_name or "ICT" in subject_name:
            return [
                { "title": "Word Processing", "lessons": [("Formatting", "Practice", 30)] },
                { "title": "Spreadsheets", "lessons": [("Formulas", "Video Lesson", 30)] }
            ]
        elif "Entrepreneurship" in subject_name:
            return [
                { "title": "Business Planning", "lessons": [("Writing a Plan", "Practice", 35)] },
                { "title": "Accounting", "lessons": [("Cash Books", "Practice", 40)] }
            ]

    elif is_alevel:
        if "Mathematics" in subject_name:
            return [
                { "title": "Pure Math: Calculus", "lessons": [("Integration", "Video Lesson", 45)] },
                { "title": "Mechanics", "lessons": [("Projectiles", "Video Lesson", 40)] }
            ]
        elif "Physics" in subject_name:
            return [
                { "title": "Advanced Mechanics", "lessons": [("Rotational Dynamics", "Video Lesson", 40)] },
                { "title": "Quantum Physics", "lessons": [("Photoelectric Effect", "Interactive Quiz", 30)] }
            ]
        elif "Chemistry" in subject_name:
            return [
                { "title": "Physical Chemistry", "lessons": [("Rate Laws", "Video Lesson", 35)] },
                { "title": "Organic Chemistry", "lessons": [("Alkanes", "Practice", 30)] }
            ]
        elif "Biology" in subject_name:
            return [
                { "title": "Genetics", "lessons": [("DNA Replication", "Simulation", 35)] },
                { "title": "Physiology", "lessons": [("Nervous System", "Video Lesson", 40)] }
            ]
        elif "Economics" in subject_name:
            return [
                { "title": "Microeconomics", "lessons": [("Demand and Supply", "Video Lesson", 35)] },
                { "title": "Macroeconomics", "lessons": [("National Income", "Practice", 40)] }
            ]
        elif "Literature" in subject_name:
            return [
                { "title": "Poetry Analysis", "lessons": [("Poetic Devices", "Video Lesson", 30)] },
                { "title": "Plays", "lessons": [("Shakespearean Tragedy", "Practice", 40)] }
            ]
        elif "Paper" in subject_name:
            return [
                { "title": "Critical Thinking", "lessons": [("Constructing Arguments", "Practice", 30)] },
                { "title": "Essay Writing", "lessons": [("Structuring an Essay", "Video Lesson", 40)] }
            ]

    return [
        { "title": f"General Introduction to {subject_name}", "lessons": [("Overview Lecture", "Video Lesson", 30)] },
        { "title": "Review of Core Principles", "lessons": [("Preparation Quiz", "Interactive Quiz", 15)] }
    ]

def populate():
    print("Starting EduClubs database seeding...")

    # 1. Fetch/Create Sections
    print("Checking Sections...")
    primary_section, _ = Section.objects.get_or_create(
        name='Primary',
        defaults={'description': 'Primary Education Section'}
    )
    secondary_section, _ = Section.objects.get_or_create(
        name='Secondary',
        defaults={'description': 'Secondary Education Section'}
    )

    # 2. Seed/Verify Levels (P.1 - P.7, S.1 - S.6)
    print("Checking Levels...")
    for i in range(1, 8):
        Level.objects.get_or_create(
            name=f'P.{i}',
            section=primary_section,
            defaults={'order': i}
        )
    for i in range(1, 5):
        Level.objects.get_or_create(
            name=f'S.{i}',
            section=secondary_section,
            defaults={'order': i + 10}
        )
    for i in range(5, 7):
        Level.objects.get_or_create(
            name=f'S.{i}',
            section=secondary_section,
            defaults={'order': i + 10}
        )

    levels = Level.objects.all().order_by('order')
    print(f"Levels in system: {[(l.id, l.name) for l in levels]}")

    # 3. Fetch/Create default user for discussion messages
    from django.contrib.auth import get_user_model
    User = get_user_model()
    default_user = User.objects.filter(is_superuser=True).first() or User.objects.first()
    if not default_user:
        default_user = User.objects.create_user(
            username="edu_explorer",
            email="explorer@edumerc.com",
            password="password123",
            first_name="Luke",
            last_name="Nyanja",
            role="STUDENT"
        )

    primary_subjects = [
        ("Mathematics", "Calculator"),
        ("English Language", "Book"),
        ("Integrated Science", "FlaskConical"),
        ("Social Studies (SST)", "Globe"),
        ("Religious Education", "BookOpen")
    ]
    olevel_subjects = [
        ("Mathematics", "Calculator"),
        ("English Language", "PenTool"),
        ("Physics", "Zap"),
        ("Chemistry", "TestTube"),
        ("Biology", "Microscope"),
        ("Geography", "Map"),
        ("History", "ScrollText"),
        ("Information and Communications Technology (ICT)", "Monitor"),
        ("Entrepreneurship Education", "Briefcase")
    ]
    alevel_subjects = [
        ("Mathematics", "Calculator"),
        ("Physics", "Zap"),
        ("Chemistry", "TestTube"),
        ("Biology", "Microscope"),
        ("Economics", "TrendingUp"),
        ("Literature in English", "BookOpen"),
        ("General Paper", "Newspaper")
    ]

    # 4. Populate Subjects, Curriculum, and Clubs
    print("Populating subjects, curriculum, and clubs...")
    for level in levels:
        if level.section == primary_section:
            subjects_to_add = primary_subjects
        elif level.name in ['S.1', 'S.2', 'S.3', 'S.4']:
            subjects_to_add = olevel_subjects
        else:
            subjects_to_add = alevel_subjects

        for idx, (sub_name, icon_name) in enumerate(subjects_to_add):
            subject, _ = Subject.objects.get_or_create(
                name=sub_name,
                level=level,
                defaults={'order': idx + 1, 'description': f"Standard {sub_name} for {level.name}"}
            )

            # Clean existing curriculum topics to prevent duplicates
            Topic.objects.filter(subject=subject).delete()

            # Create dynamic Ugandan curriculum topics and lessons
            topics_data = get_ugandan_curriculum(level.name, sub_name)
            for t_idx, topic_info in enumerate(topics_data):
                topic = Topic.objects.create(
                    title=topic_info["title"],
                    subject=subject,
                    description=f"Standard unit covering {topic_info['title']} in {sub_name}.",
                    order=t_idx + 1
                )
                subtopic = Subtopic.objects.create(
                    title=f"Core Concepts: {topic.title}",
                    topic=topic,
                    description=f"Detailed study elements of {topic.title}.",
                    order=1
                )
                for l_idx, (l_title, l_type, l_duration) in enumerate(topic_info["lessons"]):
                    s2_note = get_s2_detailed_notes(sub_name, topic.title, l_title)
                    if level.name == 'S.2' and s2_note:
                        lesson_content = s2_note
                    else:
                        lesson_content = (
                            f"### {l_title} Study Note\n\n"
                            f"Welcome to the module on **{l_title}**. Here, we discuss the core fundamentals of "
                            f"**{topic.title}** according to the Ugandan National Curriculum (NCDC) guidelines.\n\n"
                            f"#### Detailed Explanation\n"
                            f"1. Review the primary definitions and equations.\n"
                            f"2. Note standard formulas and complete practical experiments.\n"
                            f"3. Attempt past paper assessments and consult tutor guidelines.\n\n"
                            f"#### Revision Checklist\n"
                            f"- [ ] Active recall of definitions.\n"
                            f"- [ ] Form study groups to discuss key exercises.\n"
                            f"- [ ] Request feedback from your verified Coach."
                        )
                    
                    lesson = Lesson.objects.create(
                        title=l_title,
                        subtopic=subtopic,
                        objectives=f"- Gain expertise in {l_title}.\n- Understand application principles.",
                        content=lesson_content,
                        duration_minutes=45 if isinstance(l_duration, int) else 30,
                        order=l_idx + 1,
                        is_published=True
                    )
                    assessment = Assessment.objects.create(
                        title=f"Quiz on {lesson.title}",
                        lesson=lesson,
                        description=f"Standard multiple-choice assessment to evaluate learning outcomes for {lesson.title}.",
                        order=1
                    )
                    
                    # Seed multiple-choice questions & options
                    s2_questions = get_s2_detailed_questions(sub_name, l_title)
                    if level.name == 'S.2' and s2_questions:
                        for q_idx, q_data in enumerate(s2_questions):
                            q = Question.objects.create(
                                assessment=assessment,
                                text=q_data["text"],
                                order=q_idx + 1
                            )
                            for c_data in q_data["choices"]:
                                Choice.objects.create(
                                    question=q,
                                    text=c_data["text"],
                                    is_correct=c_data["is_correct"]
                                )
                    else:
                        q1 = Question.objects.create(
                            assessment=assessment,
                            text=f"What is the primary concept covered in the lesson: '{lesson.title}'?",
                            order=1
                        )
                        Choice.objects.create(question=q1, text="The correct core definition of this topic.", is_correct=True)
                        Choice.objects.create(question=q1, text="An unrelated concept.", is_correct=False)
                        Choice.objects.create(question=q1, text="A completely wrong alternative.", is_correct=False)
                        
                        q2 = Question.objects.create(
                            assessment=assessment,
                            text=f"Which of the following is true regarding '{lesson.title}'?",
                            order=2
                        )
                        Choice.objects.create(question=q2, text="True statement matching syllabus guidelines.", is_correct=True)
                        Choice.objects.create(question=q2, text="False statement.", is_correct=False)

            # Create Club with deterministic ID and direct Subject ForeignKey link
            club_id = level.id * 100 + (idx + 1)
            description = f"Connect with other students interested in {sub_name}. Improve your performance in {level.name} examinations."
            
            club, created = Club.objects.get_or_create(
                id=club_id,
                defaults={
                    'name': sub_name,
                    'icon': icon_name,
                    'description': description,
                    'level': level,
                    'type': 'subject',
                    'popular': (idx == 0 or idx == 2)
                }
            )
            club.subject = subject
            club.save()
            
            if created:
                print(f"  Created Club: {club.name} (ID: {club.id}) for Level: {level.name}")
                
                # Seed Club Notes
                Note.objects.create(
                    club=club,
                    header=f"Core Concepts of {sub_name}",
                    content=f"### Study Guide for {sub_name}\n\nWelcome to the {sub_name} club notes. In this module, we focus on the essential topics required for {level.name} assessments.\n\n#### Key Objectives\n1. Master the standard formulas and theories.\n2. Apply concepts to NCDC mock paper queries.\n3. Collaborate with study groups to review past questions."
                )
                Note.objects.create(
                    club=club,
                    header=f"{sub_name} Revision Notes",
                    content=f"### Revision Strategy\n\nEnsure you active-recall these sections:\n- Use flashcards for core terms.\n- Attempt the practice quizzes at the end of each lesson.\n- Reach out to our verified coaches for prompt support."
                )

                # Seed Role Models
                if "Math" in sub_name:
                    role_models = [
                        ("Katherine Johnson", "NASA Mathematician whose orbital calculations were critical to US spaceflights.", "https://upload.wikimedia.org/wikipedia/commons/6/6d/Katherine_Johnson_1983.jpg"),
                        ("Isaac Newton", "Physicist who developed calculus and classical mechanics.", "https://upload.wikimedia.org/wikipedia/commons/3/39/GodfreyKneller-IsaacNewton-1689.jpg")
                    ]
                elif "English" in sub_name or "Literature" in sub_name:
                    role_models = [
                        ("Chinua Achebe", "Renowned Nigerian novelist who wrote 'Things Fall Apart'.", "https://upload.wikimedia.org/wikipedia/commons/1/10/Chinua_Achebe_-_Buffalo_2008_1.jpg"),
                        ("William Shakespeare", "Classic English playwright and poet.", "https://upload.wikimedia.org/wikipedia/commons/a/a2/Shakespeare.jpg")
                    ]
                elif "Science" in sub_name or "Physics" in sub_name or "Chemistry" in sub_name:
                    role_models = [
                        ("Albert Einstein", "Theoretical physicist who formulated the theory of relativity.", "https://upload.wikimedia.org/wikipedia/commons/3/3e/Einstein_1921_by_F_Schmutzer_-_restoration.jpg"),
                        ("Marie Curie", "Pioneered radioactivity research and won two Nobel Prizes.", "https://upload.wikimedia.org/wikipedia/commons/c/c8/Marie_Curie_c._1920s.jpg")
                    ]
                elif "Biology" in sub_name:
                    role_models = [
                        ("Dr. Jane Goodall", "World-renowned primatologist and environmental activist.", "https://upload.wikimedia.org/wikipedia/commons/8/87/Jane_Goodall_2015.jpg"),
                        ("Charles Darwin", "Famous naturalist who proposed the theory of evolution.", "https://upload.wikimedia.org/wikipedia/commons/2/2e/Charles_Darwin_seated_crop.jpg")
                    ]
                else:
                    role_models = [
                        ("Prof. Apolo Nsibambi", "Eminent Ugandan scholar and statesman.", "https://images.unsplash.com/photo-1537511446984-935f663eb1f4?auto=format&fit=crop&q=80&w=200"),
                        ("Wangari Maathai", "Nobel laureate and founder of Green Belt Movement.", "https://upload.wikimedia.org/wikipedia/commons/6/64/Wangari_Maathai_2001_1.jpg")
                    ]

                for name, contribution, img in role_models:
                    RoleModel.objects.create(
                        club=club,
                        name=name,
                        contribution=contribution,
                        image=img
                    )

                # Seed Practical Project with download guide URL
                PracticalProject.objects.update_or_create(
                    club=club,
                    defaults={
                        'title': f"Hands-on {sub_name} Project",
                        'description': f"Conduct a self-guided practical project to explore {sub_name} in action.",
                        'steps': [
                            "Review current class notes and guidelines.",
                            "Gather simple household materials.",
                            "Perform the experiment / write the summary.",
                            "Share your findings in the Discussion forum for coach review."
                        ],
                        'guide_url': "https://edumerc.up.railway.app/media/guides/sample_guide.pdf"
                    }
                )

                # Seed Discussion Comments with user ForeignKeys
                DiscussionMessage.objects.create(
                    club=club,
                    user=default_user,
                    comment=f"Hello! When are we starting the revision topic for {sub_name}?",
                    time=timezone.now() - timedelta(hours=2)
                )
                DiscussionMessage.objects.create(
                    club=club,
                    user=default_user,
                    comment=f"We will begin Term 1 reviews next Monday. Check study resources in the sidebar!",
                    time=timezone.now() - timedelta(hours=1)
                )

    print("EduClubs database seeding completed successfully!")

if __name__ == "__main__":
    populate()
