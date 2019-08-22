
import java.util.Random;

import java.util.Scanner;

public class GradeCalculator {
	int classSize;
	Student classList[]; // set size of array
	Student Student;
	public int assignment1Weight;
	public int assignment2Weight;
	public int finalExamWeight;
	int studentID;
	int userChoice;

	public static int menu() {
		System.out.println("Grade Calculator (Version 0.1). Author: [Zac Burns]");

		Scanner sc = new Scanner(System.in);
		System.out.println(
				"1 - Simulate Course Marks \n	2- View/Update Student Marks \n Run Mark Statistics \n Select option [1,2,3] (9 to quit)");
		int userChoice = sc.nextInt();

		if (userChoice != 1 || userChoice != 2 || userChoice != 3 || userChoice != 9) {
			do {
				System.out.println("Please enter options: 1,2,3 or 9");
				userChoice = sc.nextInt();
			} while (userChoice != 1 || userChoice != 2 || userChoice != 3 || userChoice != 9);
		} // end if
		return userChoice;
	} // end menu method

	public void main(String[] args) {
		// implement program flow and user interface
		// call methods

		int userChoice = menu(); //this limits the options to only be 1,2,3 or 9

		while (userChoice == 1 || userChoice == 2 || userChoice == 3 || userChoice == 9) {

			if (userChoice == 1) {
				Scanner choice = new Scanner(System.in);
				System.out.println("Enter course enrollment size: ");
				classSize = choice.nextInt();
				classList = new Student[classSize];

				for (int i = 0; i < classSize; i++) {
					Student newStudent = new Student(studentID);
					classList[i] = newStudent;
					System.out.println(classList[i].getStudentNumber()); //checks to see if it connects the student number to the object
				} //

				do {
					System.out.println("Enter Assignment 1 weight (20-30)");
					assignment1Weight = choice.nextInt();
				} while (assignment1Weight < 20 || assignment1Weight > 30);

				do {
					System.out.println("Enter Assignment 2 weight (20-30)");
					assignment2Weight = choice.nextInt();
				} while (assignment2Weight < 20 || assignment2Weight > 30);

				do {
					System.out.println("Enter Final Exam weight (40-60)");
					finalExamWeight = choice.nextInt();
				} while (finalExamWeight < 20 || finalExamWeight > 30);
				
				if ((assignment1Weight + assignment2Weight + finalExamWeight) != 100) {
					System.out.println("These weights do not add up to 100%");
					userChoice = menu();
				} else {
					userChoice = menu();
				} // end if
				
			} // end if
		

			if (userChoice == 2) {
				if (classSize <= 0) {
					System.out.println(" << Error: empty class" + "list >> Run option 1 first");
					userChoice = menu();
				// calling the menu to reappear if the classSize entered is less than or equal
				// to 0
			} 	else {

				System.out.println("Enter student number");
				Scanner sc = new Scanner(System.in);
				studentID = sc.nextInt();
				if (Student.status == false) {
					System.out.println("Invalid student number entered");
					userChoice = menu();
				} else {
					System.out.println("View or Update (V/U)");
					String input = sc.nextLine();
					if (input == "V" || input == "v") {
						System.out.println("Student Number: " + Student.studentNumber + "Assignment 1 Mark: "
								+ Student.assignment1Mark + "Assignment 2 Mark: " + Student.assignment2Mark
								+ "Final Exam Mark: " + Student.finalExamMark);
					} else {
						System.out.println("Mark Type? (A1, A2, or FE): ");
						String input2 = sc.nextLine();
						if (input == "A1") {
							System.out.println("[Assignment 1] is " + Student.assignment1Mark);

						} else if (input == "A2") {
							System.out.println("[Assignment 2] is " + Student.assignment2Mark);
						} else if (input == "FE") {
							System.out.println("[Final Exam] is " + Student.finalExamMark);
						} else {
							System.out.println("[" + input + "] is an invalid mark type");
							menu();
						}
					}

				} // end else line 98

			if (userChoice == 3) {

				}
			} // end else statement 

			if (userChoice == 9) {
				System.exit(0);
			}

			else {
				System.out.println("Invalid menu selection");
				userChoice = menu();
			}

		} // end userChoice == 2
		
		} //end while
	} // end main

	// how to reference objects and classes from other file
	
	public Student generateStudentMarks(int studentID) {
		Student newStudent = new Student(studentID);
		Random random = new Random(System.currentTimeMillis());
		newStudent.assignment1Mark = random.nextInt(100) + 0;
		newStudent.assignment2Mark = random.nextInt(100) + 0;
		newStudent.finalExamMark = random.nextInt(100) + 0;
		classList[classList.length] = newStudent; //adds a new element to the end of the list
		return Student;
	}

	public int computeStudentGrade(Student aStudent) {
		int finalGrade = aStudent.assignment1Mark * (assignment1Weight / 100)
				+ aStudent.assignment2Mark * (assignment2Weight / 100)
				+ aStudent.finalExamMark * (finalExamWeight / 100);
		return finalGrade;
	}

	public void printClassReport(int[] classList, Student aStudent) {
		// how to return all object attributes
		System.out.println("Student Number " + "	A1 [" + assignment1Weight + "]" + "A2 [" + assignment2Weight + "]"
				+ "FE [" + finalExamWeight + "]" + "Final Mark");
		int i;
		for (i = 0; i < classList.length; i++) {
			System.out.println(Student.studentNumber + Student.assignment1Mark + Student.assignment2Mark
					+ Student.finalExamMark + Student.FinalGrade);
			// print out each studentNumber, and grades here
		}

	}
}
