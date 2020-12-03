# car rental system

#
----**Team Members:** Fei Hu, Jie Wang

----**Brief introduction:** This car rental system is finished by Flask, wtform, bootstrap... as package, Sqlalchemy as the database for user, Mysql as the database for storage, python as programming language. The rental system allows user to book the car and let manager easily operate the storage which including adding, editing, deleting the car. The database is connected between the customer and the manager. For example, if manager adds a new car into system, it will pop up when customer check the certain car type.  

----**File map：**
> app
>> templates(html). 

>> __init__.py. 

>> models.py. 

>> form.py. 

>> route.py. 

> config.py. 

> requirements.txt. 

> run.py  

----**Demo gif:**   

login page
![](https://github.com/ITworkonline/car_rental_system/blob/main/gif/login.gif)  

manager operation page  
![](https://github.com/ITworkonline/car_rental_system/blob/main/gif/manager_page.gif) 

customer booking page  
![](https://github.com/ITworkonline/car_rental_system/blob/main/gif/customer.gif)   
 









----**Demo Codes:**  
Enum RollType(Order.java): This helped us to define the type of the roll.
```java
public enum RollType {
		Egg,
		Pastry,
		Sausage,
		Spring,
		Jelly,
	}
```
Factory Pattern: Switching to genby its types
```java
public class FoodFactory {
	public static Food createFoodRoll(Order.RollType a) {
		Food food = null;
		switch(a) {
		case Egg: a = Order.RollType.Egg; food = new EggRoll(); break;
		case Pastry: a = Order.RollType.Pastry; food = new PastryRoll(); break;
		case Sausage: a = Order.RollType.Sausage; food = new SausageRoll();break;
		case Spring: a = Order.RollType.Spring; food = new SpringRoll();break;
		case Jelly: a = Order.RollType.Jelly; food = new JellyRoll();break;
	}
	return food;
}
}
```  
Decorator Pattern: adding behavior to each extra
```java
public abstract class ToppingDecorator extends Food {
	Food food;
	public abstract String getDescription();
	public Order.RollType getRollType(){
		return food.getRollType();
	}
}
```

----**Issues or problems:**
We also face some issues or problemencountered in this project. For example, how to pass every customer's order to the current storage, and then check if the certain roll storage finished the requirement. And if not, for causal and catering customers, we have to switch the roll type. For business customers, we have to talk him "Can't make the order".  

To solve this issues, we mainly used two functions: checkIfCasualOk(), checkIfCateringOk(), and pickAnother():
checkIfCasualOk() is checking the raw request from customers in the storage. If we still got this roll which is greater or equal to 1, we directly charged from our storage by the certain type. If the number of certain roll was equal to 0, then we used pickAnother() to see if other type of roll finished the requirement. If not, we just returned NULL and remove the request from the list.  

Here is the code for these two functions:  
checkIfCasualOk():  
```java
public void checkIfCasualOk(ArrayList<Food> a){
		for (int i = 0; i< a.size(); i++) {
			if(storeAssis.getFoodCount(a.get(i).getRollType())>=1) {
				storeAssis.chargeFoodCount(a.get(i).getRollType());
			}else {
				outage+=1;
				Food k = pickAnother();
				if(k != null) {
				a.set(i, k);
				}
				else {
					a.remove(i);
				}
			}
		}
}
```
pickAnother():  
```java
public Food pickAnother(){
		Random rand = new Random();
		Food roll = null;
		ArrayList<RollType> m = new ArrayList<RollType>();
		if(storeAssis.foodCounts[0]>0) {
			m.add(Order.RollType.Egg);
		}if(storeAssis.foodCounts[1]>0) {
			m.add(Order.RollType.Pastry);
		}if(storeAssis.foodCounts[2]>0) {
			m.add(Order.RollType.Sausage);
		}if(storeAssis.foodCounts[3]>0) {
			m.add(Order.RollType.Spring);
		}if(storeAssis.foodCounts[4]>0) {
			m.add(Order.RollType.Jelly);
		}
		int index = m.size();
		if(index ==0) {
			return null;
		}
		int rollTypeIndex = rand.nextInt(index);
		roll = FoodFactory.createFoodRoll(m.get(rollTypeIndex));
		storeAssis.chargeFoodCount(roll.getRollType());
		//System.out.println("charge by cater!");

		return roll;
	}
	
```
----**Instruction of running**:  

All of our test script is in the test.java. It includes the new instances and main function. 


