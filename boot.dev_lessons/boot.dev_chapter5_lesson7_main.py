# Boot.dev Chapter 5, Lesson 7 - Debugging Practice

# Let's complete the unlock_achievement function. It accepts 3 arguments:

# before_xp: int
# ach_xp: int
# ach_name: str

# It should return 2 values:
# The player's xp after the achievement is unlocked (The sum of before_xp and ach_xp)
# An alert message that says "Achievement Unlocked: ACHIEVEMENT_NAME", where ACHIEVEMENT_NAME is the name of the achievement
# Let's start by running the code in its current state. You should see an error like this:

# IndentationError: expected an indented block after function definition

# Hmm... looks like we're getting a syntax error: Python doesn't allow you to have an empty function body. 
# To get past this error, let's just return two dummy values from the function:

# def unlock_achievement(before_xp, ach_xp, ach_name):
#    return None, None

# Run the code again. This time you shouldn't get a syntax error, but your tests should fail because you're returning the incorrect values. Let's fix that.

# Let's start by calculating the new amount of xp. Update the function body:

# def unlock_achievement(before_xp, ach_xp, ach_name):
   # after_xp = before_xp - ach_xp
   # print("After xp:", after_xp)
   # return None, None

# Run the code again. This time you should see the after_xp value printed to the console. Does it look correct? It shouldn't... we have a bug! 
# The after_xp should be the sum of the before_xp and ach_xp values. Fix the code and run it again to make sure it's working.

# Once that's working, remove the print statement and return the after_xp value instead of the first None. Run the code again. 
# You should see that your tests are closer: The first "expected" and "actual" values should match for each test. The second return value is still broken, let's fix it!

# Now that we have the after_xp value, we need to create an alert message. Update the function body:

# def unlock_achievement(before_xp, ach_xp, ach_name):
 #   after_xp = before_xp + ach_xp
 #   alert = "Achievement: " + ach_name
 #   print(alert)
 #   return after_xp, None

# Run the code. Is the console output what you expect? We want the alert to say:

# Achievement Unlocked: ACHIEVEMENT_NAME

# Looks like the output is missing the word "Unlocked". Fix the bug, then run the code again to make sure it's working.

# When you're confident, remove the print statement and return the alert value instead of the second None. Run the code again. You should see that your tests are passing!

# Now that your tests are passing, submit your code so that it runs against all the test cases. 
# Remember, when you "run" instead of submit you're only able to see a few of the tests. 
# The submit button will run all the tests, which might catch bugs you didn't know you had! 
# That's why it's important to debug with print statements and the run button before submitting.


def unlock_achievement(before_xp, ach_xp, ach_name):
    after_xp = before_xp + ach_xp
    alert = "Achievement Unlocked: " + ach_name
    return after_xp, alert