# Ask for Height, Weight, Gender, Age, type of Meal, and Activity Level
height = float(input("Please input your height(cm): "))
weight = float(input("Please input your weight(kg): "))
gender = input("Please input your gender(F/M): ")
age = int(input("Please input your age: "))
meal = input("Which meal is it? (B for Breakfast / L for Lunch / D for Dinner): ")
print()
print("For your reference: ")
print("Sedentary: little or no exercise, desk job")
print("Moderately active: moderate exercise/ sports 6-7 days/week")
print("Very active: hard exercise every day, or exercising 2 hours/day")
print("Extra active: hard exercise 2 or more times per day, or training for marathon, or triathlon, etc")
activity_level = input("What is your activity level? (S for Sedentary / L for Lightly active / M for Moderately active / V for Very active / E for Extra active): ")

# Calculate recommended total calories by gender
if gender == "M":
    calories_needed =  66.5 + 13.8*weight + 5.0*height - 6.8*age
else:
    calories_needed = 655.1 + 9.6*weight + 1.9*height - 4.7*age
# Calculate recommended total calories by activity level
if activity_level == "S":
    calories_needed *= 1.2
elif activity_level == "L":
    calories_needed *= 1.375
elif activity_level == "M":
    calories_needed *= 1.55
elif activity_level == "V":
    calories_needed *= 1.725
else:
    calories_needed *= 1.9

# Calculate the recommended calories for the meal
if meal == "B": # 25-30% of daily calories for breakfast
    calories_lower = calories_needed*0.25
    calories_upper = calories_needed*0.30
elif meal == "L": # 35-40% of daily calories for lunch
    calories_lower = calories_needed*0.35
    calories_upper = calories_needed*0.40
else: #25-30% of daily calories for dinner
    calories_lower = calories_needed*0.25
    calories_upper = calories_needed*0.30
  
# Calculate recommended # of grams for each nutrition
carb_needed_lower = calories_lower*0.4/4
protein_needed_lower = calories_lower*0.3/4
fat_needed_lower = calories_lower*0.3/9

carb_needed_upper = calories_upper*0.4/4
protein_needed_upper = calories_upper*0.3/4
fat_needed_upper = calories_upper*0.3/9

# Optimization
import cvxpy as cp

c = cp.Variable(5,nonneg = True)   # ounce of carb 
p = cp.Variable(2,nonneg = True)   # ounce of protein
ps = cp.Variable(1, integer = True) # num of salmon （1 salmon = 7.18 ounce)
v = cp.Variable(4,nonneg = True)   # ounce of vegetable
s = cp.Variable(4,nonneg = True)   # ounce of sauce

# we want to minimize the price of the meal
obj_func = 9.5 * ((c[0]+c[1]+c[2]+c[3]+c[4])+(p[0]+p[1])+(v[0]+v[1]+v[2]+v[3])+(s[0]+s[1]+s[2]+s[3]))/16 + 4.5*ps# divide 16 for converting ounce to pound

constraints = []

constraints.append(c[0]+c[1]+c[2]+c[3]+c[4] >= 0)
constraints.append(p[0]+p[1] >= 0)
constraints.append(v[0]+v[1]+v[2]+v[3] >= 4) # at least 4 ounces of vegetables for each meal
constraints.append(s[0]+s[1]+s[2]+s[3] >= 0)
constraints.append(ps >= 0)

# lower bound 
constraints.append(8.17*c[0]+5.71*c[1]+5.83*c[2]+4.33*c[3]+6*c[4]+0.33*p[0]+1.25*p[1]+1*v[0]+1*v[1]+2*v[2]+3*v[3]+5*s[0]+5*s[1]+2*s[2]+2*s[3]+0*ps >= carb_needed_lower*0.95)
constraints.append(0.83*c[0]+0.46*c[1]+1.33*c[2]+1*c[3]+0*c[4]+6*p[0]+3*p[1]+0*v[0]+0*v[1]+0*v[2]+0*v[3]+0*s[0]+0*s[1]+2*s[2]+3*s[3]+33*ps >= protein_needed_lower*0.95)
constraints.append(0.25*c[0]+0.03*c[1]+0.58*c[2]+1*c[3]+0*c[4]+1.67*p[0]+2*p[1]+1*v[0]+0*v[1]+2*v[2]+0*v[3]+1*s[0]+1*s[1]+1.5*s[2]+0*s[3]+34*ps>= fat_needed_lower*0.95)
constraints.append(38.33*c[0]+24.57*c[1]+33.33*c[2]+31.67*c[3]+25*c[4]+43.33*p[0]+35*p[1]+20*v[0]+10*v[1]+25*v[2]+15*v[3]+30*s[0]+25*s[1]+20*s[2]+15*s[3]+440*ps >= calories_lower)

# upper bound 
constraints.append(8.17*c[0]+5.71*c[1]+5.83*c[2]+4.33*c[3]+6*c[4]+0.33*p[0]+1.25*p[1]+1*v[0]+1*v[1]+2*v[2]+3*v[3]+5*s[0]+5*s[1]+2*s[2]+2*s[3]+0*ps <= carb_needed_upper*1.05)
constraints.append(0.83*c[0]+0.46*c[1]+1.33*c[2]+1*c[3]+0*c[4]+6*p[0]+3*p[1]+0*v[0]+0*v[1]+0*v[2]+0*v[3]+0*s[0]+0*s[1]+2*s[2]+3*s[3]+33*ps <= protein_needed_upper*1.05)
constraints.append(0.25*c[0]+0.03*c[1]+0.58*c[2]+1*c[3]+0*c[4]+1.67*p[0]+2*p[1]+1*v[0]+0*v[1]+2*v[2]+0*v[3]+1*s[0]+1*s[1]+1.5*s[2]+0*s[3]+34*ps <= fat_needed_upper*1.05)
constraints.append(38.33*c[0]+24.57*c[1]+33.33*c[2]+31.67*c[3]+25*c[4]+43.33*p[0]+35*p[1]+20*v[0]+10*v[1]+25*v[2]+15*v[3]+30*s[0]+25*s[1]+20*s[2]+15*s[3]+440*ps <= calories_upper)


problem = cp.Problem(cp.Minimize(obj_func),constraints)

problem.solve(solver=cp.GUROBI,verbose = False)
print()
print("Price for this meal (without dinning dollar) = ")
print(obj_func.value)
print("Price for this meal (with dinning dollar) = ")
print(obj_func.value*0.65)
print("Calories for this meal: ")
print((38.33*c[0]+24.57*c[1]+33.33*c[2]+31.67*c[3]+25*c[4]+43.33*p[0]+35*p[1]+20*v[0]+10*v[1]+25*v[2]+15*v[3]+30*s[0]+25*s[1]+20*s[2]+15*s[3]+440*ps).value)
print("c = ")
print(c.value)
print("p = ")
print(p.value)
print("ps = ")
print(ps.value)
print("v = ")
print(v.value)
print("s = ")
print(s.value)
