
public interface CalculateLoad {

	public boolean haveEnoughLoadCapacity(Integer massToShip);
	public Integer calculateRemainCapacity();
	public boolean haveSameDest(String cityName);
	public String shipToString();

}
