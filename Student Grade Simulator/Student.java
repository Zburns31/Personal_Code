import java.util.Random;

public class Student {
	int studentNumber;
	boolean status;
	int assignment1Mark;
	int assignment2Mark;
	int finalExamMark;
	String markType;
	int studentID;
	int Mark;
	int FinalGrade;
	boolean studentStatus;
	

	
	public Student(int studentID) {
		
		if (setStudentNumber(studentID)) {
			//if setStudentNumber returns true given this studentID input by the user, execute the block of code below
			

			Random rand = new Random();
			studentNumber = rand.nextInt(99999999) + 10000000;
			assignment1Mark = rand.nextInt(100);
			assignment2Mark = rand.nextInt(100);
			finalExamMark = rand.nextInt(100);
			studentStatus = true;
			status = true;
			
		
	}
		
		
			
		
		
		

		
	}
	//add weight and integer value constraints
	public boolean updateMark(String markType, int Mark, int Weight) {
		if (Mark > 100 || Mark < 0) {
			return false ;  //how to set constraints for method parameters
		}
		
		if (this.markType == "A1") {
			assignment1Mark = Mark;
			return true;
		}
		else if (this.markType == "A2") {
			assignment2Mark = Mark;
			return true;
		}
		else if (this.markType == "FE") {
			finalExamMark = Mark;
			return true;
		}
			return false;
			
	}
	
	public int getMark(String markType) {
		if (markType == "A1") {
			return Mark;
		}
		else if (markType == "A2") {
			return Mark;
		}
		else if (markType == "FE") {
			return Mark;
		}
		else {
			return -1;
		}
	}
	
	public int getStudentNumber() { 
		return studentNumber;
	}
	
	public boolean getStatus() {
		return status;
	}
	
	public int getRandom() {
		Random random = new Random();
		int randomNumber = random.nextInt(9999999- 10000000) + 1000000; 
		studentNumber = randomNumber;
		return studentNumber;
		
	}
	
	public boolean setStudentNumber(int studentNumber) {
		if ( studentNumber >= 10000000 && studentNumber <= 99999999) {
			status = true;
			//if it returns false, then student id is inactive or not assigned
			//set student number to a random number between the parameters set
		} else {
			status = false;
		}
		return status;
	}

} //end class
