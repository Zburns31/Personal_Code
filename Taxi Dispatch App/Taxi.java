
public class Taxi extends Vehicle implements CalculateDistance{

	protected Integer cX;
	protected Integer cY;
	
	public Taxi(Integer sID, Integer vID, Integer x, Integer y) {
		super(sID, vID);
		cX = x;
		cY = y;
	}
	
	public Integer getCX() {
		return cX;
	}
	public Integer getCY() {
		return cY;
	}
	
	public String toString() {
		return super.toString()+", cX="+cX+", cY="+cY;
	}

	public double distToCaller(Integer x, Integer y) {
		return Math.sqrt((cX-x)*(cX-x)+(cY-y)*(cY-y));
	}
	public String distToString(Integer x, Integer y) {
		return super.toString()+", distance to caller="+Math.sqrt((cX-x)*(cX-x)+(cY-y)*(cY-y));
	}
}
