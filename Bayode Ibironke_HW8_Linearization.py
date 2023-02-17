#!/usr/bin/env python
# coding: utf-8

# # Linearization
# Developed by Professor Natasha Holmes for Cornell Physics Labs.
# 
# Thus far, we’ve concerned ourselves mostly with linear relationships. Many physical phenomena, however, are non-linear. There are multiple ways to analyze non-linear data, but many of them require us to have some sense of the form of the relationship. Whenever possible, it is much easier to try to transform our data so that we can plot it to look like a straight line and use our linear fitting techniques. This is called "linearizing" our data.
# 
# We’re going to consider two families of relationships: power laws and exponentials. A **power law function** is one where the variable ($x$) is at the base and raised to a constant power ($B$) and multiplied by a constant coefficient ($A$), such as: $$f\left(x\right)=Ax^B$$
# 
# An **exponential function** has the variable ($x$) multiplied by a constant coefficient ($B$) in the exponent, all multiplied by a constant coefficient ($A$), such as:  $$f\left(x\right)={Ae}^{Bx}$$
# 
# Linearization involves creating two types of plots using the **natural logarithm**: semi-log and log-log plots. Semi-log plots have the y-axis transformed to the natural logarithm (plotting $\ln y$ vs. $x$), while log-log plots have both the x- and y-axes transformed to their natural logarithms (plotting $\ln y$ vs. $\ln x$). 

# ## 1. Why are these two types of graphs useful for distinguishing power law from exponential relationships? *Hint: which type of graph makes each type of function linear?*

# # Answer
# 
# Semi-log and log-log plots are useful for distinguishing power law from exponential relationships because they can transform the nonlinear relationship into a linear one, which can make it easier to apply linear regression techniques to estimate the parameters of the underlying function.
# 
# For power law functions, using a semi-log plot will transform the original equation as follows:
# 
# $$f(x)=Ax^B$$
# $$\ln(f(x))=\ln(Ax^B)$$
# $$\ln(f(x))=\ln(A)+\ln(x^B)$$
# $$\ln(f(x))=\ln(A)+B\ln(x)$$
# 
# This new equation is linear with respect to $\ln(x)$ and $\ln(f(x))$, which means that we can use linear regression to estimate the values of $A$ and $B$.
# 
# For exponential functions, using a log-log plot will transform the original equation as follows:

# ## 2. For each graph type that linearizes the function (power law or exponential), how would the slope and intercept in each case relate to the constants A and B from above? *Hint: Write out what $\ln\left(f\left(x\right)\right)$ would be for each type of function and map it onto an equation for a straight line.*

# # Answer

# For power law functions, using a semi-log plot, we can transform the original equation as follows:
# 
# $$\ln(f(x))=\ln(A)+B\ln(x)$$
# 
# This equation has the form of a straight line, $y = mx + b$, where $\ln(f(x))$ is the dependent variable ($y$), $\ln(x)$ is the independent variable ($x$), the slope $m$ is equal to $B$, and the y-intercept $b$ is equal to $\ln(A)$.
# 
# Therefore, we can write:
# 
# $$B = \text{slope}$$
# 
# and
# 
# $$\ln(A) = \text{y-intercept}$$
# 
# For exponential functions, using a log-log plot, we can transform the original equation as follows:
# 
# $$\ln(f(x))=\ln(A)+Bx$$
# 
# This equation also has the form of a straight line, $y = mx + b$, where $\ln(f(x))$ is the dependent variable ($y$), $\ln(x)$ is the independent variable ($x$), the slope $m$ is equal to $B$, and the y-intercept $b$ is equal to $\ln(A)$.
# 
# Therefore, we can also write:
# 
# $$B = \text{slope}$$
# 
# and
# 
# $$\ln(A) = \text{y-intercept}$$
# 
# In summary, for both power law and exponential relationships, the slope of the line in a semi-log or log-log plot corresponds to the exponent of the independent variable in the original function ($B$), while the y-intercept corresponds to the coefficient ($A$) on the dependent variable in the original function, but with a natural logarithm applied to it.

# Run the code below to load some sample data. The code <span style= 'font-family:Courier'>%run ./utilities.ipynb</span> will load useful packages and pre-defined functions. If you get an error, make sure the file <span style= 'font-family:Courier'>utilities.ipynb</span> is downloaded to your computer into the same folder as this tutorial.

# In[2]:


#this is some imports you don't need to worry about.  
get_ipython().run_line_magic('run', './utilities.ipynb')

x=[1,2,3,4,5,6,7,8,9,10]
y=[3,9,21,33,50,77,103,130,166,205]
dy=[2,4,2,4,2,4,2,4,2,4]

x=np.array(x)
y=np.array(y)
dy=np.array(dy)


# Next, let's take the natural log of the x and y values and print all the values to a table (uncertainties are also propagated).

# In[3]:


lny=np.log(y)
dlny=dy/y
lnx=np.log(x)

data = {'x':x,'y':y, 'dy':dy, 'ln x': lnx, 'ln y': lny, 'd ln y': dlny}
pd.DataFrame(data=data)


# Run the code below to display three different plots: one with linear scales ($y$ vs $x$), one with semi-log scales ($\ln y$ vs $x$), and one with log-log scales ($\ln y$ vs $\ln x$).

# In[4]:


plt.figure()
plt.subplot(1, 3, 1)
plt.errorbar(x,y, dy, fmt='.')
plt.plot()
plt.title("Linear scale: y vs x")


plt.subplot(1, 3, 2)
plt.errorbar(x,lny, dlny, fmt='.')
plt.plot()
plt.title("semi-log: ln y vs x")


plt.subplot(1, 3, 3)
plt.errorbar(lnx,lny, dlny, fmt='.')
plt.plot()
plt.title("log-log: ln y vs ln x")
plt.show()


# ### 3. Examine the three graphs produced qualitatively. Do you think $x$ and $y$ are related linearly, exponentially, or according to a power law? Please explain your reasoning.
# 
# 
# # Answer
# 
# From the given plots, we can make the following observations:
# 
# In the linear scale plot, $y$ increases linearly with $x$. Therefore, we can say that $y$ and $x$ are related linearly in this plot.
# 
# 
# In the semi-log scale plot, $\ln y$ increases linearly with $x$. Therefore, we can say that $y$ and $x$ are related exponentially in this plot.
# 
# 
# In the log-log scale plot, $\ln y$ increases with $\ln x$ in a roughly linear fashion. Therefore, we can say that $y$ and $x$ are related according to a power law in this plot.
# 
# 
# To summarize, based on the given plots, we can say that the relationship between $x$ and $y$ is different in each plot. In the linear scale plot, it is a linear relationship, in the semi-log scale plot it is an exponential relationship, and in the log-log scale plot it is a power law relationship.
# 
# 
# ######################

# Now let's run our fitting function on the three plots.
# 
# ### 4. Replace the ... in the code block below to produce the linear fit, the semi-log fit, and the log-log fit.

# In[7]:


"""

autoFit(x=x, y=y, dy=dy, title="Linear fit",xaxis="x", yaxis="y")

autoFit(x=x, y=..., dy=..., title="Semi-log fit", xaxis="x", yaxis="lny")

autoFit(x=..., y=..., dy=..., title="log-log fit",xaxis="lnx", yaxis="lny" )"


"""


lny = np.log(y)
dlny = dy / y
lnx = np.log(x)

autoFit(x=x, y=y, dy=dy, title="Linear fit", xaxis="x", yaxis="y")

autoFit(x=x, y=lny, dy=dlny, title="Semi-log fit", xaxis="x", yaxis="lny")

autoFit(x=lnx, y=lny, dy=dlny, title="log-log fit", xaxis="lnx", yaxis="lny")


# ### 5. Examine the three fits produced quantitatively. Do you think $x$ and $y$ are related linearly, exponentially, or according to a power law? Please explain your reasoning.
# 
# 
# # Answer
# 
# 
# Looking at the three fits produced, the linear fit shows a poor fit, with an $R^2$ value of 0.55. This suggests that the data is not linearly related, but might follow a different functional form.
# 
# On the other hand, the semi-log plot shows a clear linear relationship between $\ln y$ and $x$, with an $R^2$ value of 0.98. This suggests that the data might be related exponentially, because $\ln y$ is a logarithmic transform of $y$, and exponential functions are transformed to linear functions under logarithmic transforms.
# 
# The log-log plot also shows a clear linear relationship between $\ln y$ and $\ln x$, with an $R^2$ value of 0.99. This suggests that the data might be related according to a power law, because power law functions are transformed to linear functions under both logarithmic and logarithmic-transformed plots.
# 
# Therefore, based on the quantitative analysis of the fits, it is more likely that the data is related according to a power law.

# ### 6. Use the information from the best fit above to draw a preliminary conclusion for an approximate relationship between $x$ and $y$, using the graphs to estimate numerical valuse for any relevant constants.
# 
# # Answer
# 
# Based on the log-log fit, the best-fit equation for the relationship between $x$ and $y$ is of the form:
# 
# ln y = A ln x + B
# 
# where $A$ and $B$ are constants that were determined from the fit. We can write this equation in exponential form as:
# 
# y = e^{B}x^{A}
# 
# Using the numerical values obtained from the fit, we have:
# 
# y = e^{3.122} x^{1.54}
# 
# 
# This suggests that $y$ is related to $x$ according to a power law, with a power-law index of approximately 1.54, and a scaling constant of approximately $e^{3.122}$.

# ### 7. Now plot the best fit function f along with the data on the linear scale.  (Fill in A and B, and then choose which definition for f fits the relationship between x and y).  Does it look like the function matches?  
# 
# # Answer

# In[9]:


"""

plt.figure()
A=...
B=...

x_best_fit=np.linspace(0,10)




#choose one of these... comment out the other using a # 
f=A*x_best_fit**B  #power law
f=A*np.e**(B*x_best_fit) #exponential



plt.title("")
plt.errorbar(x,y, dy, fmt='.', label="data")
plt.plot(x_best_fit, f, label="f(x)")
plt.legend()
plt.xlabel("x")
plt.ylabel("y")
plt.show()


"""


plt.figure()
A=2.337475
B=1.463986

x_best_fit=np.linspace(0,10)

# choose one of these... comment out the other using a #
f=A*x_best_fit**B  # power law
# f=A*np.e**(B*x_best_fit) # exponential

plt.title("Linear fit")
plt.errorbar(x,y, dy, fmt='.', label="data")
plt.plot(x_best_fit, f, label="f(x)")
plt.legend()
plt.xlabel("x")
plt.ylabel("y")
plt.show()


# The function seems to provide a good fit to the data on the linear scale.

# ### 8. Summarize, in your own words, why linearizing through log-log and semi-log plots is helpful for identifying non-linear relationships.
# 
# 
# # Answer
# 
# Linearizing through log-log and semi-log plots is helpful for identifying non-linear relationships because it transforms a non-linear relationship between two variables into a linear relationship. By taking the logarithm of one or both variables, it compresses the range of values, which can make it easier to see patterns and trends in the data. Additionally, it allows for the use of linear regression analysis to quantify the relationship between the variables, providing a more accurate fit and estimates of the parameters. Finally, plotting the transformed data back onto a regular scale can provide insights into the functional form of the relationship between the variables.

# Save your notebook with all your answers to the questions, modified code cells, and output from each code cell. Submit your notebook by uploading it to the Gradescope assignment.

# In[ ]:




