
public class Truck extends Vehicle implements CalculateLoad{

	protected String assignedDest;
	protected Integer maxLoad;
	protected Integer currentLoad;
	protected Integer originalLoad;
	protected boolean inUse;
	
	public Truck(Integer sID, Integer vID, String ad, Integer ml, Integer cl) {
		super(sID, vID);
		assignedDest = ad;
		maxLoad = ml;
		currentLoad = cl;
		originalLoad = cl;
		inUse = false;
	}
	
	public String getAssignedDest() {
		return assignedDest;
	}
	public Integer getMaxLoad() {
		return maxLoad;
	}
	public Integer getCurrentLoad() {
		return currentLoad;
	}
	public Integer getOriginalLoad() {
		return originalLoad;
	}
	public void setCurrentLoad(Integer n) {
		currentLoad = n;
	}
	public boolean getInUse() {
		return inUse;
	}
	public void setInUse() {
		inUse = true;
	}
	
	public String toString() {
		return super.toString()+", assignedDest="+assignedDest+",maxLoad="+maxLoad+"kg, currentLoad="+currentLoad+"kg";
	}

	public String shipToString() {
		Integer n1 = maxLoad-originalLoad;
		Integer n2 = maxLoad-currentLoad;
		return super.toString()+", assignedShip="+currentLoad+"kg, unusedBeforeShip="+n1+"kg, unusedAfterShip"+n2+"kg";
	}
	public boolean haveEnoughLoadCapacity(Integer massToShip) {
		return (maxLoad-currentLoad>=massToShip);
	}
	public Integer calculateRemainCapacity() {
		return (maxLoad-currentLoad);
	}
	public boolean haveSameDest(String cityName) {
		return (assignedDest.equals(cityName));
	}
}
