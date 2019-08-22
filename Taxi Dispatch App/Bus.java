
public class Bus extends Vehicle implements HaveSeat{

	protected Integer currentMileage;
	protected Integer seatNum;
	
	public Bus(Integer sID, Integer vID, Integer cm, Integer sn) {
		super(sID, vID);
		currentMileage = cm;
		seatNum = sn;
	}
	
	public Integer getCurrentMileage() {
		return currentMileage;
	}
	public Integer getSeatNum() {
		return seatNum;
	}
	
	public String toString() {
		return super.toString()+", currentMileage="+currentMileage+", seatNum="+seatNum;
	}

	public boolean haveEnoughSeats(Integer num) {
		return (seatNum>=num);
	}
}
