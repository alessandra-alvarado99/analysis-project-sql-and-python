import sqlite3
import pandas as pd
import matplotlib.pyplot as plt



with sqlite3.connect("database/Northwind.db") as conn:
    #TOP 10 SELLING PRODUCTS
    
    query= """SELECT ProductName, SUM(Price * Quantity) as Revenue
    FROM OrderDetails od
    JOIN Products p ON p.ProductID = od.ProductID
    GROUP BY od.ProductID
    ORDER BY Revenue DESC
    LIMIT 10 """
    
    top_products = pd.read_sql_query(query,conn)
    top_products.plot(x="ProductName", y="Revenue", kind= "bar", figsize=(10,5), legend= False)
    plt.title("TOP 10 SELLING PRODUCTS")
    plt.xlabel("Products")
    plt.ylabel("Revenue")
    plt.xticks(rotation= 90)
   
    #TOP 5 MOST EFFECTIVE EMPLOYEES
    
    query2= """
    SELECT FirstName || " " || LastName as Employee, COUNT(*) as Total 
    FROM Orders o
    JOIN Employees e
    ON e.EmployeeID = o.EmployeeID
    GROUP BY o.EmployeeID
    ORDER BY Total DESC
    LIMIT 5
    """

    top_employees_e= pd.read_sql_query(query2,conn)
    top_employees_e.plot(x= "Employee", y="Total", kind= "bar", figsize= (10,5), legend= False )
    plt.title("TOP 5 MOST EFFECTIVE EMPLOYEES")
    plt.xlabel("Employees")
    plt.ylabel("Sales volume")
    plt.xticks(rotation= 45)
    
    #TOP 5 MOST EFFECTIVE EMPLOYEES (MONETARY AMOUNT COLLECTED)
    query3= """
    SELECT (SELECT FirstName || " " || LastName FROM Employees WHERE EmployeeID= O.EmployeeID) as Name,
    round(sum(quantity* (SELECT Price FROM Products WHERE ProductID= OD.ProductID) )) as Amount
    FROM OrderDetails OD
    JOIN Orders O
    ON OD.OrderID = O.OrderID
    GROUP BY Name
    ORDER BY Amount DESC
    LIMIT 5
    """
    top_employees_r= pd.read_sql_query(query3,conn)
    top_employees_r.plot(x= "Name", y="Amount", kind= "bar", figsize= (10,5), legend= False )
    plt.title("TOP 5 MOST EFFECTIVE EMPLOYEES")
    plt.xlabel("Employees")
    plt.ylabel("Total amount (USD)")
    plt.xticks(rotation= 45)
    
    
plt.show()
