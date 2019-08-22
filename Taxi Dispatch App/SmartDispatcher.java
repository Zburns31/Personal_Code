import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.PrintWriter;
import java.util.Scanner;
import java.util.StringTokenizer;
import java.lang.Math;

public class SmartDispatcher {

	public static void main(String[] args) {

		String fileName;
		System.out.println("Starting ... ");
		
//		final usage report output file
		PrintWriter outReportFile = null;
		fileName = "C:/Users/BlueGreen/eclipse-workspace/SmartDispatcher/src/finalUsageReport.txt";
		try {
			outReportFile = new PrintWriter(new FileOutputStream(fileName));
		}
		catch (FileNotFoundException e) {
			System.out.println("Could not open file "+fileName +" --- Exiting");
			System.out.println("Message from Exception object = "+e.getMessage()); // every Exception object has a getMessage() method
			System.exit(0);
		}

//		bus selection output file
		PrintWriter outBusSelectionFile = null;
		fileName = "C:/Users/BlueGreen/eclipse-workspace/SmartDispatcher/src/BusSelections.txt";
		try {
			outBusSelectionFile = new PrintWriter(new FileOutputStream(fileName));
		}
		catch (FileNotFoundException e) {
			System.out.println("Could not open file "+fileName +" --- Exiting");
			System.out.println("Message from Exception object = "+e.getMessage()); // every Exception object has a getMessage() method
			System.exit(0);
		}

//		taxi selection output file
		PrintWriter outTaxiSelectionFile = null;
		fileName = "C:/Users/BlueGreen/eclipse-workspace/SmartDispatcher/src/TaxiSelections.txt";
		try {
			outTaxiSelectionFile = new PrintWriter(new FileOutputStream(fileName));
		}
		catch (FileNotFoundException e) {
			System.out.println("Could not open file "+fileName +" --- Exiting");
			System.out.println("Message from Exception object = "+e.getMessage()); // every Exception object has a getMessage() method
			System.exit(0);
		}

//		truck selection output file
		PrintWriter outTruckSelectionFile = null;
		fileName = "C:/Users/BlueGreen/eclipse-workspace/SmartDispatcher/src/TruckSelections.txt";
		try {
			outTruckSelectionFile = new PrintWriter(new FileOutputStream(fileName));
		}
		catch (FileNotFoundException e) {
			System.out.println("Could not open file "+fileName +" --- Exiting");
			System.out.println("Message from Exception object = "+e.getMessage()); // every Exception object has a getMessage() method
			System.exit(0);
		}

//		input files
		Scanner inFile = null;			
		String inLine;
		StringTokenizer st;
		int stateID, vehicleID, currentMileage, seatNum, busStateCount, requiredSeatNum, busCallCount, busNumWithEnoughSeats, totalMileage;
		int averageMileage,busStateNum, mileageDiff, locationX, locationY, taxiStateCount, taxiCallCount, taxiStateNum;
		int maxLoad, currentLoad, truckStateCount, truckStateNum, mass, remainCapacity, truckCallCount;
		double minDistance;
		String destCity;
		int i,j;
		Bus[] bus = new Bus[200];
		Taxi[] taxi = new Taxi[500];
		Truck[] truck = new Truck[200];

//		open busStates.txt file
		System.out.println("Reading busStates.txt file ... ");
		try {
			inFile = new Scanner(new FileInputStream("C:/Users/BlueGreen/eclipse-workspace/SmartDispatcher/src/busStates.txt"));
		} // end try
		catch (FileNotFoundException e) {
			System.out.println("Message from exception = "+e.getMessage());
			System.exit(0);
		}// end catch
		
		i=1;
		while (inFile.hasNextLine()) {
			inLine = inFile.nextLine();		// read a line of file
//			System.out.println("inLine = "+inLine);
			st = new StringTokenizer(inLine,"\t");
			stateID = Integer.parseInt(st.nextToken());
			vehicleID = Integer.parseInt(st.nextToken());
			currentMileage = Integer.parseInt(st.nextToken());
			seatNum = Integer.parseInt(st.nextToken());
//			System.out.println(i+" stateID="+stateID+", vehicleID="+vehicleID+", currentMileage="+currentMileage+", seatNum="+seatNum);
			bus[i++] = new Bus(stateID, vehicleID, currentMileage, seatNum);
		}
		busStateCount = i-1;
	
//		open taxiStates.txt file
		System.out.println("Reading taxiStates.txt file ... ");
		try {
			inFile = new Scanner(new FileInputStream("C:/Users/BlueGreen/eclipse-workspace/SmartDispatcher/src/taxiStates.txt"));
		} // end try
		catch (FileNotFoundException e) {
			System.out.println("Message from exception = "+e.getMessage());
			System.exit(0);
		}// end catch
		
		i=1;
		while (inFile.hasNextLine()) {
			inLine = inFile.nextLine();		// read a line of file
//			System.out.println("inLine = "+inLine);
			st = new StringTokenizer(inLine,"\t");
			stateID = Integer.parseInt(st.nextToken());
			vehicleID = Integer.parseInt(st.nextToken());
			locationX = Integer.parseInt(st.nextToken());
			locationY = Integer.parseInt(st.nextToken());
//			System.out.println(i+" stateID="+stateID+", vehicleID="+vehicleID+", locationX="+locationX+", locationY="+locationY);
			taxi[i++] = new Taxi(stateID, vehicleID, locationX, locationY);
		}
		taxiStateCount = i-1;
	
//		open truckStates.txt file
		System.out.println("Reading truckStates.txt file ... ");
		try {
			inFile = new Scanner(new FileInputStream("C:/Users/BlueGreen/eclipse-workspace/SmartDispatcher/src/truckStates.txt"));
		} // end try
		catch (FileNotFoundException e) {
			System.out.println("Message from exception = "+e.getMessage());
			System.exit(0);
		}// end catch
		
		i=1;
		while (inFile.hasNextLine()) {
			inLine = inFile.nextLine();		// read a line of file
//			System.out.println("inLine = "+inLine);
			st = new StringTokenizer(inLine,"\t");
			stateID = Integer.parseInt(st.nextToken());
			vehicleID = Integer.parseInt(st.nextToken());
			destCity = st.nextToken();
			maxLoad = Integer.parseInt(st.nextToken());
			currentLoad = Integer.parseInt(st.nextToken());
//			System.out.println(i+" stateID="+stateID+", vehicleID="+vehicleID+", destCity="+destCity+", maxLoad="+maxLoad+", currentLoad="+currentLoad);
			truck[i++] = new Truck(stateID, vehicleID, destCity, maxLoad, currentLoad);
		}
		truckStateCount = i-1;
	
//		open busCalls.txt file
		System.out.println("Reading busCalls.txt file ... ");
		System.out.println("Processing busCalls ... ");
		try {
			inFile = new Scanner(new FileInputStream("C:/Users/BlueGreen/eclipse-workspace/SmartDispatcher/src/busCalls.txt"));
		} // end try
		catch (FileNotFoundException e) {
			System.out.println("Message from exception = "+e.getMessage());
			System.exit(0);
		}// end catch
		i=1;
		while (inFile.hasNextLine()) {
			inLine = inFile.nextLine();		// read a line of file
//			System.out.println("inLine = "+inLine);
			st = new StringTokenizer(inLine,"\t");
			stateID = Integer.parseInt(st.nextToken());
			destCity = st.nextToken();
			requiredSeatNum = Integer.parseInt(st.nextToken());
//			System.out.println(i+" stateID="+stateID+", destCity="+destCity+", requiredSeatNum="+requiredSeatNum);
			totalMileage = busNumWithEnoughSeats = 0;
			for (j=1;j<busStateCount;j++) {
				if (bus[j].getStateID()==stateID && bus[j].haveEnoughSeats(requiredSeatNum) && bus[j].getAvailable()) {
					totalMileage+=bus[j].getCurrentMileage();
					busNumWithEnoughSeats++;
				}
			}
			if (totalMileage == 0) 
				outBusSelectionFile.println("BusRequest("+"stateID="+stateID+", destCity="+destCity+", requiredSeatNum="+requiredSeatNum+") cannot be statisfied.");
//				System.out.println("BusRequest("+"stateID="+stateID+", destCity="+destCity+", requiredSeatNum="+requiredSeatNum+") cannot be statisfied.");
			else {
				averageMileage = totalMileage/busNumWithEnoughSeats;
				mileageDiff = totalMileage;
				busStateNum = 0;
				for (j=1;j<busStateCount;j++) {
					if (bus[j].getStateID()==stateID && bus[j].haveEnoughSeats(requiredSeatNum) && bus[j].getAvailable()
							&& Math.abs(bus[j].getCurrentMileage()-averageMileage) <= mileageDiff) busStateNum = j;
				}
				outBusSelectionFile.println(bus[busStateNum].toString());
//				System.out.println(bus[busStateNum].toString());
				bus[busStateNum].setNotAvailable();
			}
			i++;
		}
		busCallCount = i-1;
	
//		open taxiCalls.txt file
		System.out.println("Reading taxiCalls.txt file ... ");
		System.out.println("Processing taxiCalls ... ");
		try {
			inFile = new Scanner(new FileInputStream("C:/Users/BlueGreen/eclipse-workspace/SmartDispatcher/src/taxiCalls.txt"));
		} // end try
		catch (FileNotFoundException e) {
			System.out.println("Message from exception = "+e.getMessage());
			System.exit(0);
		}// end catch
		i=1;
		while (inFile.hasNextLine()) {
			inLine = inFile.nextLine();		// read a line of file
//			System.out.println("inLine = "+inLine);
			st = new StringTokenizer(inLine,"\t");
			stateID = Integer.parseInt(st.nextToken());
			locationX = Integer.parseInt(st.nextToken());
			locationY = Integer.parseInt(st.nextToken());
//			System.out.println(i+" stateID="+stateID+", locationX="+locationX+", locationY="+locationY);
			taxiStateNum = 0;
			minDistance = 999999999;
			for (j=1;j<taxiStateCount;j++) {
				if (taxi[j].getStateID()==stateID && taxi[j].distToCaller(locationX, locationY)<=minDistance && taxi[j].getAvailable()) {
					minDistance = taxi[j].distToCaller(locationX, locationY);
					taxiStateNum = j;
				}
			}
			if (minDistance == 999999999) 
				outTaxiSelectionFile.println("TaxiRequest("+"stateID="+stateID+", locationX="+locationX+", locationY="+locationY+") cannot be statisfied.");
//				System.out.println("TaxiRequest("+"stateID="+stateID+", locationX="+locationX+", locationY="+locationY+") cannot be statisfied.");
			else {
				outTaxiSelectionFile.println(taxi[taxiStateNum].distToString(locationX, locationY));
//				System.out.println(taxi[taxiStateNum].distToString(locationX, locationY));
				taxi[taxiStateNum].setNotAvailable();
			}
			i++;
		}
		taxiCallCount = i-1;
	
//		open truckCalls.txt file
		System.out.println("Reading truckCalls.txt file ... ");
		System.out.println("Processing truckCalls ... ");
		try {
			inFile = new Scanner(new FileInputStream("C:/Users/BlueGreen/eclipse-workspace/SmartDispatcher/src/truckCalls.txt"));
		} // end try
		catch (FileNotFoundException e) {
			System.out.println("Message from exception = "+e.getMessage());
			System.exit(0);
		}// end catch
		i=1;
		while (inFile.hasNextLine()) {
			inLine = inFile.nextLine();		// read a line of file
//			System.out.println("inLine = "+inLine);
			st = new StringTokenizer(inLine,"\t");
			stateID = Integer.parseInt(st.nextToken());
			destCity = st.nextToken();
			mass = Integer.parseInt(st.nextToken());
//			System.out.println(i+" stateID="+stateID+", destCity="+destCity+", mass="+mass);
			remainCapacity = 0;
			truckStateNum = 0;
			for (j=1;j<truckStateCount;j++) {
				if (truck[j].getStateID()==stateID && truck[j].haveSameDest(destCity) && truck[j].haveEnoughLoadCapacity(mass) 
						&& truck[j].calculateRemainCapacity()>=remainCapacity && truck[j].getAvailable()) {
					remainCapacity = truck[j].calculateRemainCapacity();
					truckStateNum = j;
				}
			}
			if (remainCapacity == 0) 
				outTruckSelectionFile.println("TruckRequest("+"stateID="+stateID+", destCity="+destCity+", mass="+mass+"kg) cannot be statisfied.");
//				System.out.println("TruckRequest("+"stateID="+stateID+", destCity="+destCity+", mass="+mass+"kg) cannot be statisfied.");
			else {
				truck[truckStateNum].setCurrentLoad(truck[truckStateNum].getCurrentLoad() + mass);
				outTruckSelectionFile.println(truck[truckStateNum].shipToString());
//				System.out.println(truck[truckStateNum].shipToString());
				truck[truckStateNum].setInUse();
				if (truck[truckStateNum].getCurrentLoad()/truck[truckStateNum].getMaxLoad() >= 0.9)	truck[truckStateNum].setNotAvailable();
			}
			i++;
		}
		truckCallCount = i-1;
		
//		final report output file
		int preStateID, vehicleCount, inUseCount;
		preStateID = 1;
		vehicleCount=inUseCount=0;
		for (i=1;i<=busStateCount;i++) {
			if (bus[i].getStateID()==preStateID) {
				vehicleCount++;
				if (!bus[i].getAvailable()) inUseCount++;
			}
			else {
				outReportFile.println("Vehicle Type=Bus, State="+preStateID+", Fleet Size="+vehicleCount+", In Use="+inUseCount);
//				System.out.println("Vehicle Type=Bus, State="+preStateID+", Fleet Size="+vehicleCount+", In Use="+inUseCount);
				preStateID++;
				vehicleCount=inUseCount=0;
			}
		}
		outReportFile.println("Vehicle Type=Bus, State="+preStateID+", Fleet Size="+vehicleCount+", In Use="+inUseCount);
//		System.out.println("Vehicle Type=Bus, State="+preStateID+", Fleet Size="+vehicleCount+", In Use="+inUseCount);

		preStateID = 1;
		vehicleCount=inUseCount=0;
		for (i=1;i<=taxiStateCount;i++) {
			if (taxi[i].getStateID()==preStateID) {
				vehicleCount++;
				if (!taxi[i].getAvailable()) inUseCount++;
			}
			else {
				outReportFile.println("Vehicle Type=Taxi, State="+preStateID+", Fleet Size="+vehicleCount+", In Use="+inUseCount);
//				System.out.println("Vehicle Type=Taxi, State="+preStateID+", Fleet Size="+vehicleCount+", In Use="+inUseCount);
				preStateID++;
				vehicleCount=inUseCount=0;
			}
		}
		outReportFile.println("Vehicle Type=Taxi, State="+preStateID+", Fleet Size="+vehicleCount+", In Use="+inUseCount);
//		System.out.println("Vehicle Type=Taxi, State="+preStateID+", Fleet Size="+vehicleCount+", In Use="+inUseCount);

		preStateID = 1;
		vehicleCount=inUseCount=0;
		for (i=1;i<=truckStateCount;i++) {
			if (truck[i].getStateID()==preStateID) {
				vehicleCount++;
				if (!truck[i].getInUse()) inUseCount++;
			}
			else {
				outReportFile.println("Vehicle Type=Truck, State="+preStateID+", Fleet Size="+vehicleCount+", In Use="+inUseCount);
//				System.out.println("Vehicle Type=Truck, State="+preStateID+", Fleet Size="+vehicleCount+", In Use="+inUseCount);
				preStateID++;
				vehicleCount=inUseCount=0;
			}
		}
		outReportFile.println("Vehicle Type=Truck, State="+preStateID+", Fleet Size="+vehicleCount+", In Use="+inUseCount);
//		System.out.println("Vehicle Type=Truck, State="+preStateID+", Fleet Size="+vehicleCount+", In Use="+inUseCount);
	
//		close input&output files
		inFile.close();
		outReportFile.close();
		outBusSelectionFile.close();
		outTaxiSelectionFile.close();
		outTruckSelectionFile.close();
		System.out.println("Processing completed.");
	}
}
