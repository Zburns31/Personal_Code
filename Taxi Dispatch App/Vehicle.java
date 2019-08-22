
public class Vehicle {
	
	protected Integer stateID;
	protected Integer vehicleID;
	protected boolean available;

	public Vehicle(Integer sID, Integer vID) {
		stateID = sID;
		vehicleID = vID;
		available = true;
	}

	public Integer getStateID() {
		return stateID;
	}
	public Integer getVehicleID() {
		return vehicleID;
	}
	public boolean getAvailable() {
		return available;
	}
	public void setNotAvailable() {
		available = false;
	}

	public String toString() {
		return "stateID="+stateID+", vehicleID="+vehicleID;
//		return "stateID="+stateID+", vehicleID="+vehicleID+", available="+available;
	}
}
