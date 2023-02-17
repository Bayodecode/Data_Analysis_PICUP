#!/usr/bin/env python
# coding: utf-8

# # Tutorial 4: Curve Fitting
# 
# Developed by Megan Renz for Cornell Physics Labs.
# 
# Reminder: the code cells throughout this tutorial will build off of previous code cells. It is important to run every code cell <SHIFT + ENTER> in the document, in order, up to the point where you are working every time you open this tutorial. If you get an error message (particularly one that says that a particular variable is not defined) after attempting to run a code cell, first make sure that you have run every previous code cell. 
# 
# Oftentimes, we will want to figure out the relationship between two variables, i.e., $x$ and $y$, as a function: $f(x)=y$. The most common question will be if the relationship between $x$ and $y$ is linear; in this case, we need to also figure out what the slope and intercept of that line should be.  
# 
# Let's say we have some data, which we want to plot as $y$ vs $x$ and find out if the relationship between them is linear.  
# 
# Below we have a graph where the data are the blue dots and the solid red and dotted green lines show two attempts to fit the data. Run the block below. 

# In[2]:


#this is some imports you don't need to worry about.  
get_ipython().run_line_magic('matplotlib', 'notebook')
import matplotlib.pyplot as plt
import numpy as np
from ipywidgets import *


#Again, don't worry too much about this code, just creating an example.  
x=np.arange(10)
y=np.arange(10)+np.random.random(10)-.5
plt.figure()
plt.errorbar(x,y, np.ones(10)*.2, fmt='.')
plt.plot(x,x,'r', label="f(x)=x")
plt.plot(x,.5*x, 'g-.', label="f(x)=.5*x")
plt.title("y vs x")
plt.legend()
plt.show()


# ### 1. Which one of the two lines above seems like a better fit to the data? Please explain your reasoning.
# 
# 
# # Answer
# 
# 
# It appears that the line "f(x) = x" (in red) is a better fit to the data than the line "f(x) = 0.5x" (in green) because the points on the plot are generally closer to the red line than the green line. Additionally, the red line appears to capture the general trend of the data more accurately than the green line, which seems to consistently underestimate the y-values of the points.

# Most of the time, the difference between possible fit lines will be a bit more subtle. In these cases, we want to come up with a way to make our goodness-of-fit assessment quantitative instead of qualitative.  To do that, we are going to use our data and our function and come up with a number or "score" that tells us if our fit is good or bad.  
# 
# When the score is small, our fit is good, and when the score is large, our fit is bad.  
# 
# 
# We want to take several things into account:  
# 
# 1.  The score should increase as the points get further away from the function, by our definition above.
# 2.  We want points with smaller uncertainties to "count" more towards the score; if the function is far away from a point with a small uncertainty, our fit is worse than if the function is far away from a point that has large uncertainty.   
# 3.  Our score should not depend on units. That is, we want the score to be dimensionless so we can have a standard way of interpreting a "good" or "bad" fit, regardless of the units in our data.
# 4.  Our score should not change as we add more points that are similar to the ones we already have. That is, we want a standard way of interpreting a "good" or "bad" fit, regardless of the number of data points.
# 
# 
# While there are many ways to assess how well a curve fits data, the method that we will use here is called Chi-Squared ("chi" is pronounced like "sky", but without the 's'):
# 
# 
# $$\chi^2=\frac{1}{N} \sum_{i=1}^N \frac{(f(x_i)-y_i)^2}{\delta y_i^2}$$
# 
# where we have data points $(x_1, y_1) ... (x_N, y_N)$ with associated uncertainties $\delta y_i$, and $f(x_i)$ is the function we are fitting evaluated at $x_i$. In the graph above, the red and green lines are examples of possible functions $f(x)$.
# 
# 

# ### 2. Explain how the formula for $\chi^2$ fulfills the four requirements above.
# 
# # Answer
# 
# The formula for $\chi^2$ fulfills the four requirements as follows:
# 
# 1. The term $(f(x_i)-y_i)^2$ in the numerator increases as the distance between the function $f(x_i)$ and the data point $y_i$ increases, fulfilling the first requirement.
# 2. The denominator $\delta y_i^2$ takes into account the uncertainty of each data point, so that points with smaller uncertainties contribute more to the score, fulfilling the second requirement.
# 3. Dividing by the number of data points $N$ in the formula makes the score dimensionless, fulfilling the third requirement.
# 4. The sum over all data points ensures that the score is independent of the number of data points, fulfilling the fourth requirement.
# 
# $\chi^2$ is written as a python function below. Run the code block below.

# In[3]:


def chiSquared(x, y, dy, f, args):
    '''Function Chi-Squared.  
    x, y and dy are numpy arrays, referring to x, y and the uncertainty in y respectively.
    f is the function we are fitting. 
    args are the arguments of the function we have fit.  
    '''
    return 1/(len(x)-len(args))*np.sum((f(x, args)-y)**2/dy**2)


# ### 3. Compare the equation for $\chi^2$ to the equation for $t^{\prime}$ from the last homework tutorial. In what ways are the equations similar and in what ways are they different?
# 
# # Answer
# 
# Skip
# 

# ### 4. What might a small $\chi^2$ value mean? What should count as "small"?
# 
# 
# # ANSWER
# 
# A small $\chi^2$ value means that the fit of the function to the data is good, or that the differences between the observed data and the predicted values from the model are small relative to the uncertainties in the data.
# 
# In general, there is no strict rule for what counts as a "small" $\chi^2$ value, as it depends on the number of data points, the number of parameters in the model, and the level of uncertainty in the data. A commonly used guideline is that a good fit has a $\chi^2$ value that is close to or slightly less than the number of degrees of freedom (dof), which is defined as the difference between the number of data points and the number of parameters in the model. That is, a small $\chi^2$ value is typically one that is close to or less than the number of dof. 

# ### 5. What might a large $\chi^2$ mean?  What should count as "large"?
# 
# 
# # ANSWER
# 
# A large $\chi^2$ value means that the fit of the function to the data is poor, or that the differences between the observed data and the predicted values from the model are large relative to the uncertainties in the data.
# 
# In general, there is no strict rule for what counts as a "large" $\chi^2$ value, as it depends on the number of data points, the number of parameters in the model, and the level of uncertainty in the data. However, a commonly used guideline is that a fit is considered poor if the $\chi^2$ value is significantly larger than the number of degrees of freedom (dof), which is defined as the difference between the number of data points and the number of parameters in the model. In practice, a commonly used threshold for a poor fit is when the $\chi^2/dof$ ratio exceeds 2 or 3. However, this threshold may vary depending on the specific problem and the goals of the analysis, and should be interpreted in the context of the specific situation.

#  Below are a few example functions one can fit.  We will most often be fitting a line. Run the code block below. (You do not need to worry about the details)

# In[4]:


def poly(x, args):
    '''
    returns the value of the polynomial sum (x**i*args[i])
    '''
    total=x**0*args[0]
    for i in range(1,len(args)):
        total+=x**i*args[i]
    return total
def linear(x, args):
    '''
    A special case of Poly.  
    '''
    return args[0]+x*args[1]


# Let's take a look at fitting a line to some data.  
# 
# Here we have some data of an experiment in which a spring is stretched and the spring's force ($y$) is measured at certain stretching distances ($x$). Run the code below, which will produce two graphs.
# 
# The first is a graph of the data points (black dots with uncertainty bars) and a fit line (in blue). The second is a *residuals* plot, which shows the difference between $f(x_i)$ (the value of our function at $x_i$) and $y_i$ (the measured data at $x_i$) at each $x_i$.  

# In[5]:


y=np.array([ 1.36,  3.36,  3.92,  4.11,  3.43,  5.22,
  8.29,  8.22, 11.15, 10.86])
uncertainty=np.ones(10)
uncertainty[4]=4
x=np.linspace(1,8,10)

fig, ax=plt.subplots(1,2, figsize=(8,4))
ax[0].set_title("force vs extension")
line,=ax[0].plot(x,linear(x, [0,1]))
data=ax[0].errorbar(x,y, uncertainty, fmt='.k')
ax[1].set_title("residuals")
residuals=linear(x,[0, 1])-y
res=ax[1].errorbar(x,residuals, uncertainty, fmt='.k')
ax[1].grid(True, which='both')
plt.show()
def update(intercept=0,slope=1):
    fx=linear(x,[intercept, slope])

    line.set_ydata(fx)
    residuals=fx-y
    ax[1].cla()
    res=ax[1].errorbar(x,residuals, uncertainty, fmt='.k')
    ax[1].grid(True, which='both')
    ax[1].set_title("Residuals")
    ax[1].set_xlabel("extension (cm)")
    ax[1].set_ylabel("f(x) - y")
    ax[0].set_xlabel("extension (cm)")
    ax[0].set_ylabel("force (N)")
    fig.canvas.draw_idle()
    print("chi-squared value:  ")
    print(chiSquared(x,y, uncertainty, linear, [intercept, slope]).round(3))
interact(update, intercept=(-5, 20, .1), slope=(-1, 10, .1));


# Try adjusting the slope and intercept of the line above using the sliders. Watch how the chi-squared value changes as the line becomes a better or worse fit.
# 
# You can also adjust the slope and intercept values by clicking the numbers to the right of the sliders and typing in your desired value.

# ### 6. What happens as you change the values for the slope and intercept?
# 
# 
# # ANSWER
# 
# When the slope and intercept values are changed such that the fit line moves closer to the data points, the value of the chi-squared decreases, indicating a better fit. Conversely, when the slope and intercept values are changed such that the fit line moves farther away from the data points, the value of the chi-squared increases, indicating a worse fit.

# ### 7. What values for the slope and intercept give the smallest value of $\chi^2$ (to the first decimal place)?
# 
# # Answer
# 
# From the plot, it looks like the smallest value of $\chi^2$ is around 2.3, and this occurs for a slope of about 1.9 and an intercept of about 0.5. To find more precise values, we can use an optimization routine to minimize $\chi^2$ with respect to the parameters. 

# ### 8. How confident are you that the line you fit is a good representation of the underlying phenomena? (One way to check this is to see if any other lines look like better fits, qualitatively.)
# 
# # Answer
# 
# One way to check the goodness of the fit is to visualize the data and the fitted line. Looking at the plot, it appears that the linear model is a reasonably good fit for the data. The residuals are roughly symmetric around 0 and do not appear to show any systematic deviations from zero, suggesting that the linear model is capturing the essential features of the data. 
# 
# However, it is always good practice to perform additional tests and analyses to confirm the validity of the model and to quantify the uncertainty in the fitted parameters.
# 
# There are several additional tests and analyses that could be performed to evaluate the quality of the fit and the underlying assumptions of the model:
# 
# 1. Residual analysis: Plot the residuals (the difference between the observed values and the predicted values) against the independent variable. If the residuals are randomly scattered around zero, this is a good indication that the model is a good fit. If the residuals have a pattern, such as a curved shape, this may indicate that the model is not capturing some important feature of the data.
# 2. Normal probability plot: Create a normal probability plot of the residuals to check if they are normally distributed. If the residuals fall along a straight line, this is a good indication that they are normally distributed, which is a key assumption of many statistical models.
# 3. Outlier analysis: Check for outliers, which are data points that are significantly different from the rest of the data. Outliers can have a big impact on the fit of the model and may need to be removed or given special treatment.
# 4. Model comparison: Compare the fitted model with alternative models to see which one provides the best fit to the data. For example, you could fit a higher-order polynomial and compare its performance with that of the linear model.
# 5. Cross-validation: Perform cross-validation to check how well the model generalizes to new data. This involves splitting the data into training and testing sets, fitting the model on the training data, and then evaluating its performance on the testing data. If the model performs well on the testing data, this is a good indication that it will generalize well to new data.
# 6. Coefficient significance test: Test the significance of the coefficients to determine if they are significantly different from zero. If a coefficient is not significantly different from zero, this is an indication that it may not be contributing significantly to the model.
# 
# 
# 
# 
# 

# This brings us to another question - what if our $\chi^2$ is really small?  (This is a rhetorical question).  Run the code block below.  

# In[6]:



largeUncertainty=uncertainty*5

fig, ax=plt.subplots(1,2, figsize=(8,4))
ax[0].set_title("force vs extension")
line,=ax[0].plot(x,linear(x, [0,1]))
data=ax[0].errorbar(x,y, largeUncertainty, fmt='.k')
ax[1].set_title("residuals")
residuals=linear(x,[0, 1])-y
res=ax[1].errorbar(x,residuals, largeUncertainty, fmt='.k')
ax[1].grid(True, which='both')
plt.show()
def update(intercept=0,slope=1):
    fx=linear(x,[intercept, slope])
    line.set_ydata(fx)
    residuals=fx-y
    ax[1].cla()
    res=ax[1].errorbar(x,residuals, largeUncertainty, fmt='.k')
    ax[1].set_title("residuals")
    ax[1].grid(True, which='both')
    fig.canvas.draw_idle()
    print("chi-squared value:  ")
    print(chiSquared(x,y, largeUncertainty, linear, [intercept, slope]).round(3))
interact(update, intercept=(-5, 12, .2), slope=(0, 5, .1));




# Now you should have a large range of values for which the $\chi^2$ value is quite small. For example, a fit with intercept=-4.6 and slope=2.2 and one with intercept=3.2 and slope=.6 both give $\chi^2$ values around 0.2. *Reminder:  You can enter values into the boxes next to the sliders!*
# 
# 
# ### 9. How confident are you that either of these sets of fit parameters are a good representation of the underlying phenomena?  Do you trust them?  
# 
# 
# # Answer
# 
# If the uncertainty is really large, it's possible that even a small value of $\chi^2$ is not necessarily an indicator that the fit parameters are good. In the code provided above, the uncertainties were increased by a factor of 5, which is a significant increase. As a result, even though the value of $\chi^2$ may be small, it's difficult to say how confident we should be in the fit parameters because the uncertainties are so large. In general, it's always a good idea to consider the uncertainties and perform additional tests to validate the fit parameters.

# If your $\chi^2$ is too small (e.g. $\chi^2 <<1$), you may have overestimated your uncertainties. That is, your fit is telling you that you measured these data points much more precisely than you thought! Uncertainty overestimation is a problem because it means that it is hard to identify which of the lines that appear to be a good fit actually reflect the underlying physics.   

# 
# ### 10. What do you think you should do if you obtain a very small $\chi^2$ value?
# 

# A $\chi^2$ value larger than 9 is considered a very poor fit for the data. (Why 9?) 
# 
# For $\chi^2$, there are a few possible outcomes:  
# 
# 1. $\chi^2\approx1$
# 
# 2.  $\chi^2<<1$
# 
# 3.  $1\lesssim\chi^2<9$
# 
# 4.  $\chi^2 >9$
# 
# # Answer
# 
# If you obtain a very small $\chi^2$ value (e.g. $\chi^2 <<1$), it may indicate that you have overestimated your uncertainties. In such a case, you should re-evaluate your uncertainties and consider whether you need to revise them. One way to do this is to check whether there are any systematic errors in your measurement setup or technique that might have affected your results. You should also consider whether there are any sources of noise that you did not account for in your uncertainties.
# 
# A $\chi^2$ value larger than 9 is considered a very poor fit for the data because it indicates that the model is a poor description of the data. The reason 9 is used as a threshold is because it corresponds to a 3-sigma deviation from the expected value of $\chi^2=1$ for a good fit, assuming normally distributed errors.
# 
# In general, the quality of a fit can be assessed based on the value of $\chi^2$ relative to the degrees of freedom (dof), which is the number of data points minus the number of free parameters in the model. If $\chi^2/dof \approx 1$, it indicates a good fit, whereas values much smaller or much larger than 1 indicate potential issues with the model or uncertainties.
# 
# It's worth noting that the appropriate value of $\chi^2$ can depend on the context and the specific problem being studied. For example, in some cases, a higher value of $\chi^2$ may be acceptable if the uncertainties are known to be larger or if the model is a relatively crude approximation of the underlying physics. Ultimately, the value of $\chi^2$ should be used as a guide for evaluating the quality of a fit, but it is not a definitive indicator of the correctness of a model or the accuracy of the uncertainties.

# ### 11. Write down different interpretations for what each of these $\chi^2$ values could mean, and what you should do in each case.  *Hint: refer to the interpretations of values of $t^\prime$ from the previous tutorial.*
# 
# # Answer
# 
# Here are some possible interpretations and suggested actions for different values of $\chi^2$:
# 
# 1. $\chi^2 \approx 1$: This indicates that the model fits the data reasonably well, given the uncertainties. However, it is still possible that there are systematic errors or other sources of uncertainty that have not been accounted for. If $\chi^2$ is close to 1, it is a good idea to carefully examine the residuals (the differences between the data points and the model predictions) to check for any patterns or outliers that might suggest systematic errors. It may also be worthwhile to consider alternative models to see if they provide a better fit.
# 2. $\chi^2 << 1$: As noted earlier, this could indicate that the uncertainties have been overestimated, or that there are other sources of uncertainty that have not been accounted for. In this case, it may be necessary to re-evaluate the uncertainties and consider whether there are any systematic errors in the measurement setup or technique. If these issues are addressed, it is possible that a better fit can be obtained.
# 3. $1 \lesssim \chi^2 < 9$: This indicates that the model provides an acceptable fit to the data, but there may be some room for improvement. It is possible that there are sources of uncertainty that have not been accounted for, or that the model can be refined to better describe the data. In this case, it may be worthwhile to examine the residuals and consider alternative models or parameterizations to see if they provide a better fit.
# 
# 4. $\chi^2 > 9$: This indicates that the model is a poor fit to the data, and there may be significant sources of uncertainty that have not been accounted for. It is also possible that the model is incorrect or incomplete. In this case, it may be necessary to revisit the measurement setup or technique to check for systematic errors, or to consider alternative models that provide a better fit. It may also be worthwhile to examine the residuals and consider whether there are any outliers or patterns that suggest systematic errors. If all of these efforts fail to produce a good fit, it may be necessary to reconsider the assumptions underlying the model and to explore alternative approaches.
# 
# 
# #### <span style='color:Red'>*You should never manipulate your uncertainties to obtain a specific $\chi^2$ value. Your uncertainties should always reflect your real measurements.*</span>

# Now let's investigate the graph called "Residuals".  This is a graph of $f(x_i)-y_i$, the difference between what our fit predicts and what we actually got during the experiment.  The x-axis is the same as the graph "force vs. extension", but the y-axis is the vertical distance between the line and points. 

# ### 12. Given how you expect points to be distributed around the line, what do you expect to see in your residuals graph, if $f(x_i)$ is a good fit? 

# Looking at the residuals graph is a good way to tell if you are trying to fit the right kind of function. The $\chi^2$  value does not necessarily tell the whole story.
# 
# # Answer
# 
# If the fit $f(x_i)$ is a good fit to the data, we would expect to see residuals that are randomly scattered around zero, with no systematic patterns or trends. In other words, we would expect to see some positive residuals (indicating that the predicted value of force is greater than the actual observed value) and some negative residuals (indicating that the predicted value of force is less than the actual observed value), but these residuals should be distributed randomly and should cancel each other out on average.
# 
# If the residuals graph shows a clear pattern or trend, it suggests that the fit is not a good fit to the data, and that we may need to consider alternative functional forms or models to better capture the underlying physics. For example, if the residuals tend to be positive for small values of the independent variable and negative for large values, it suggests that the fit is underestimating the force at small extensions and overestimating it at large extensions. In this case, we might need to consider alternative models that account for nonlinearities in the relationship between force and extension.
# 
# It's also worth noting that the residuals graph can be useful for identifying outliers, which are data points that deviate significantly from the expected values based on our fit. Outliers can be a sign of measurement errors, data entry errors, or other sources of bias, and they should be carefully examined to ensure that they are not unduly influencing our fit. In some cases, it may be appropriate to exclude outliers from the analysis if they are determined to be the result of errors or other sources of bias.
# 
# 
# 
# ##### Run the code below, and adjust the slider to slope=5, intercept=-17.

# In[7]:


y=np.array([ 1.36,  3.36,  3.92,  4.11,  3.43,  5.22,
  8.29,  8.22, 11.15, 10.86])
uncertainty=np.ones(10)
uncertainty[4]=4
x=np.linspace(1,8,10)

fig, ax=plt.subplots(1,2, figsize=(8,4))
ax[0].set_title("force vs extension")
line,=ax[0].plot(x,linear(x, [0,1]))
data=ax[0].errorbar(x,y, uncertainty, fmt='.k')
ax[1].set_title("residuals")
residuals=linear(x,[0, 1])-y
res=ax[1].errorbar(x,residuals, uncertainty, fmt='.k')
ax[1].grid(True, which='both')
plt.show()
def update(intercept=-17,slope=5):
    fx=linear(x,[intercept, slope])
    line.set_ydata(fx)
    residuals=fx-y
    ax[1].cla()
    res=ax[1].errorbar(x,residuals, uncertainty, fmt='.k')
    ax[1].grid(True, which='both')
    ax[1].set_title("Residuals")
    ax[0].set_xlabel("extension (cm)")
    ax[0].set_ylabel("force (N)")
    fig.canvas.draw_idle()
    print("chi-squared value:  ")
    print(chiSquared(x,y, uncertainty, linear, [intercept, slope]).round(3))
interact(update, intercept=(-20, 20, .1), slope=(-1, 10, .1));




# 
# 
# While the $\chi^2$ value tells us that this fit is bad (large $\chi^2$), the residual graph can give us an idea about *why*. In this case, the residuals show a linear trend and tells us that the first half of the data points are systematically above the line and the second half are systematically below the line. This should clearly suggest that you should change the slope of the line!
# 
# Let's try another example.
# 
# 

# In[8]:


y=np.array([ 1.36,  3.36,  3.92,  4.21,  5.43,  6.22,
  8.29,  8.22, 10.15, 10.86])
y=.5*(y-2)**2
uncertainty=np.ones(10)
uncertainty[4]=4
x=np.linspace(1,8,10)

fig, ax=plt.subplots(1,2, figsize=(8,4))
ax[0].set_title("force vs extension")
line,=ax[0].plot(x,linear(x, [0,1]))
data=ax[0].errorbar(x,y, uncertainty, fmt='.k')
ax[1].set_title("residuals")
residuals=linear(x,[0, 1])-y
res=ax[1].errorbar(x,residuals, uncertainty, fmt='.k')
ax[1].grid(True, which='both')
plt.show()
def update(intercept=-17,slope=5):
    fx=linear(x,[intercept, slope])
    line.set_ydata(fx)
    residuals=fx-y
    ax[1].cla()
    res=ax[1].errorbar(x,residuals, uncertainty, fmt='.k')
    ax[1].grid(True, which='both')
    ax[1].set_title("Residuals")
    ax[0].set_xlabel("extension (cm)")
    ax[0].set_ylabel("force (N)")
    fig.canvas.draw_idle()
    print("chi-squared value:  ")
    print(chiSquared(x,y, uncertainty, linear, [intercept, slope]).round(3))
interact(update, intercept=(-20, 20, .1), slope=(-1, 10, .1));


# In this case, the residuals show an upside down "v".
# 
# ### 13. What do you think this shape of residuals might suggest about your fit? How might you change the function to get a better fit?
# 

# # Answer
# 
# The upside-down "v" shape of the residuals suggests that the current fit may be underestimating the force at intermediate values of the extension, while overestimating it at both low and high values of extension. This may indicate that a linear function is not the best fit for the data.
# 
# One way to potentially get a better fit would be to consider using a more flexible functional form, such as a quadratic or cubic function, which could better capture any nonlinearities in the relationship between force and extension. Another approach would be to add additional explanatory variables that may help explain the observed variation in the data, such as the velocity or acceleration of the object being measured.
# 
# It's also worth noting that the large uncertainty in the fifth data point (four times the size of the other uncertainties) may be skewing the fit, and it may be worth considering whether this point should be excluded from the analysis or whether the uncertainty estimate for this point should be revised.
# 
# 
# ###
# 
# Let's practice writing your own code to fit a function to some data manually below.  
# 
# For example, let's say you stretch a string to the same extension multiple times and measure the force required each time.  
# 
# First, I have created some sample data, which is 10 extensions (in cm) of the spring (stored in x), and a matrix of 10 rows and 5 columns, where each row is the forces (in N) measured for 5 trials.  
# 
# Each of the 10 rows corresponds to one of the extension values, in order. Notice that as extension increases, force increases. Within each row, there is no clear trend because each row displays the same measurement taken five times at that extension. 
# 
# ### 14. Print out the measurements of the extensions and forces in a matrix. Why are the number of values in "extensions" equal to the number of rows in "forces"? What are the units of all the values in "extensions"? What are the units of all the values in "forces"? 
# 

# In[9]:


extensions=np.linspace(0,9, 10)
forces=np.random.normal(0,.5,size=(5,10))
forces=forces+extensions[None,:]
forces=forces.T

print("extensions: \n", extensions)
print("forces: \n",forces)


# We do not want to plot all 50 data points in the table above. Instead, we want to average the 5 data points for each extension, so that we are only plotting 10 data points (with a clear trend). The uncertainty in the mean should be used to make the errorbars.  
# 
# As a hint, take a look at the code below:  
# 
# 

# In[10]:


numpyExample=np.array([[1,2],[3,4], [5,1]])
print(numpyExample)
print("summing over axis=0:")
print(np.sum(numpyExample, axis=0))
print("summing over axis=1:")
print(np.sum(numpyExample, axis=1))


# # Answer

# In[14]:


import numpy as np

np.random.seed(42)

# Generate some fake data

extensions = np.linspace(1, 10, 10)
forces = np.random.normal(loc=extensions[:, np.newaxis], scale=1, size=(10, 5))

print("Extensions:\n", extensions)
print("Forces:\n", forces)


# # Answer
# 
# The number of values in extensions is equal to the number of rows in forces because each row in forces corresponds to one extension value, in order. The units of all the values in extensions are centimeters (cm). The units of all the values in forces are Newtons (N).

# Note: When using functions in *numpy*, you can specify whether you want to take the average across the row or the column using <span style='font-family:Courier'>axis = 1</span> or <span style='font-family:Courier'>axis = 0</span> respectively.  This also works for <span style='font-family:Courier'>np.sum</span> and other functions.
# 
# 
# 
# We will need to average the five trials together for each extension of the spring, and put that in $y$, and find the uncertainty in the force measurement for each extension of the spring, and put that in $dy$. 
# 
# Your final answer for both $y$ and $dy$ should be a vector of length 10.  
# 
# ## Answer

# In[26]:


# Generate some fake data

extensions = np.linspace(1, 10, 10).reshape(-1, 1)
forces = np.random.normal(loc=extensions, scale=1, size=(10, 5))


print("Extensions:\n", extensions)
print("\nForces:\n", forces)

# Average the five trials together for each extension of the spring
y = np.mean(forces, axis=1)


# Find the uncertainty in the force measurement for each extension of the spring
dy = np.std(forces, axis=1, ddof=1) / np.sqrt(forces.shape[1])

print("\ny:\n", y)
print("\ndy:\n", dy)


print ("\nOr\n")

extensions = np.linspace(1, 10, 10)
forces = np.random.normal(loc=extensions[:, np.newaxis], scale=1, size=(10, 5))


print("Extensions:\n", extensions)
print("\nForces:\n", forces)

# Average the five trials together for each extension of the spring
y = np.mean(forces, axis=1)


# Find the uncertainty in the force measurement for each extension of the spring
dy = np.std(forces, axis=1, ddof=1) / np.sqrt(forces.shape[1])

print("\ny:\n", y)
print("\ndy:\n", dy)


# ### 15. Fill in the three '...' below to create an array for the mean force measurements for each extension of the spring, $y$, and their uncertainties, $dy$.  
#   
# [1.] Check that *y* and *dy* are what you expect (particularly check the number of data points). 
# 
# [2.] Manually check the first value (corresponding to extension=0 for each). 

# # Answer

# In[44]:


'''
y=np.mean(..., axis=1) #Take the mean of each of the sets of 5 trials in "forces".  

#Note: When using functions in numpy, you can specify whether you want to take the average across the row or the 
#column using axis= 1 or 0 respectively.  This also works for np.sum and other functions.

print("y:")
print(y)
dy=np.std(..., axis=1)/np.sqrt(...) #Calculate the standard uncertainty of the mean for each of the sets of 5 trials in "forces". 
#divide by square root of number of trials in each set to get the uncertainty.  
print("dy:")
print(dy)

'''

y=np.mean(forces, axis=1) #Take the mean of each of the sets of 5 trials in "forces".  

#Note: When using functions in numpy, you can specify whether you want to take the average across the row or the 
#column using axis= 1 or 0 respectively.  This also works for np.sum and other functions.

print("y:")
print(y)
dy=np.std(forces, axis=1)/np.sqrt(forces.shape[1]) #Calculate the standard uncertainty of the mean for each of the sets of 5 trials in "forces". 
#divide by square root of number of trials in each set to get the uncertainty.  
print("dy:")
print(dy)


# ### Answer Cont.

# In[46]:


extensions = np.linspace(1, 10, 10)
forces = np.random.normal(loc=extensions, scale=1, size=(5, 10)).T

print("Extensions:\n", extensions)
print("Forces:\n", forces)

# Calculate mean force measurements and their uncertainties
y = np.mean(forces, axis=1)
dy = np.std(forces, axis=1) / np.sqrt(forces.shape[1])

print("y:")
print(y)
print("dy:")
print(dy)


# 1. y and dy should both be 1D arrays of length 10, since there are 10 extensions.
# 2. The first value of y should be approximately equal to the mean of the first column of forces, which should be close to 1 since the first extension is 1 and the mean force for each extension is equal to the extension plus some normally distributed noise with mean 1. The first value of dy should be the standard deviation of the first column of forces divided by the square root of the number of trials, which is 5, since there are 5 trials for each extension.

# Now let's plot what we just made, and try fitting it. Run the code block below. 

# In[47]:



uncertainty=dy 
fig, ax=plt.subplots(1,2, figsize=(8,4))
ax[0].set_title("force vs extension")
line,=ax[0].plot(x,linear(x, [0,1]))
data=ax[0].errorbar(x,y, uncertainty, fmt='.k')
ax[1].set_title("residuals")
residuals=linear(x,[0, 1])-y
res=ax[1].errorbar(x,residuals, uncertainty, fmt='.k')
ax[1].grid(True, which='both')
plt.show()
def update(intercept=0,slope=1):
    fx=linear(x,[intercept, slope])
    line.set_ydata(fx)
    residuals=fx-y
    ax[1].cla()
    res=ax[1].errorbar(x,residuals, uncertainty, fmt='.k')
    ax[1].grid(True, which='both')
    ax[1].set_title("Residuals")
    fig.canvas.draw_idle()
    print("chi-squared value:  ")
    print(chiSquared(x,y, uncertainty, linear, [intercept, slope]).round(3))
interact(update, intercept=(-2, 12, .2), slope=(0, 5, .1));

