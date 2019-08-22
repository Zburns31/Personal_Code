// Zac Burns | 10140192 | CISC 124
import java.io.FileNotFoundException;
import java.util.Scanner;
import java.io.FileInputStream;
import java.util.StringTokenizer;
import java.io.FileOutputStream;
import java.io.PrintWriter;
import java.util.NoSuchElementException;

public class fileReader {

	public static void main(String[] args) {

		// Here I am creating the Error output file for bad lines of text in the songs
		// file
		String outFile;

		PrintWriter errorFile = null; // initializing error file object
		outFile = "error.txt";

		try {
			errorFile = new PrintWriter(new FileOutputStream(outFile));
		} // end try statement
		catch (FileNotFoundException e) {
			System.out.println("File : " + errorFile + "could not be found. Program exiting...");
			System.out.println("Error Message : " + e.getMessage()); // use .getMessage method for exception object
			System.exit(0);
		} // end catch block
		errorFile.println("Song ID ---> (Error Message)"); // prints out the bad lines in the songs file
		errorFile.println("----------------------------");

		// This code block below creates the output file for song_category.txt. It is
		// surrounded by a try/catch block to catch a FileNotFound exception
		PrintWriter song_categoryOutFile = null;
		outFile = "song_category.txt";
		try {
			song_categoryOutFile = new PrintWriter(new FileOutputStream(outFile));
		} catch (FileNotFoundException e) {
			System.out.println("File : " + song_categoryOutFile + "could not be found. Program exiting...");
			System.out.println("Error Message : " + e.getMessage()); // every Exception object has a getMessage() method
			System.exit(0);
		}
		song_categoryOutFile.println("Song ID ---> (Error Message)");
		song_categoryOutFile.println("----------------------------");

		// This code block below contains the code to create the output file
		// category_stats.txt
		PrintWriter outFile_CategoryStats = null;
		outFile = "category_stats.txt";
		try {
			outFile_CategoryStats = new PrintWriter(new FileOutputStream(outFile));
		} catch (FileNotFoundException e) {
			System.out.println("File : " + outFile_CategoryStats + "could not be found. Program exiting...");
			System.out.println("Error Message : " + e.getMessage()); // every Exception object has a getMessage() method, use that here to display the error message
			System.exit(0);
		}
		outFile_CategoryStats.println("Category ID --- (Stats) --- Song");
		outFile_CategoryStats.println("--------------------------------");

		// this code below opens and reads the categories file to import the song
		// categories into the program

		String inLine;
		Scanner inFile = null;
		int[][] songCategories = new int[10][8]; // Max of 10 categories and 7 columns needed: 1 for ID, 6 for category 

		int[] minSongDistance = new int[10]; // store the lowest distance for each category in this variable
		int lineCount = 0;
		int col = 0;
		int numberofCategories = 0; // this variable will be used to count the number of categories
		StringTokenizer st; // Using this string tokenizer to split each line of input from text file

		System.out.println("Program beginning...reading song categories ");
		// this try block attempts to open the categories file
		try {
			inFile = new Scanner(new FileInputStream("categories"));

		} catch (FileNotFoundException e) {
			System.out.println("Message from exception = " + e.getMessage());
			System.out.println("Program exiting...");
			System.exit(0);
		} // end catch block

		System.out.println("File opened");
		// while the file object has a next line, set inLine = the next line
		while (inFile.hasNextLine()) {
			inLine = inFile.nextLine();

			st = new StringTokenizer(inLine, ",");
			for (col = 0; col < 7; col++) {
				songCategories[lineCount][col] = Integer.parseInt(st.nextToken());
			} // end for loop
			
			songCategories[lineCount][col] = 0; // initialize the value --> this is to store the number of songs that is
			// closest to this category
			minSongDistance[lineCount] = 999999; // initialize the value -- this stores the minimum song distance from each
			lineCount++; // category
		} // end while loop
		numberofCategories = lineCount;
		inFile.close();
		System.out.println("File reading finished ");

		// try/catch statements for reading the Songs file

		try {
			inFile = new Scanner(new FileInputStream("Songs"));
			System.out.println("Song File opened");

		} catch (FileNotFoundException e) {
			System.out.println("Message from exception = " + e.getMessage());
			System.out.println("Program exiting...");
			System.exit(0);
		}

		String songID; // variable to store the song name
		String[] songsArray = new String[10]; // this is for storing the song ID that is closest to a category
		int[] songAspectValues = new int[6];
		int distance;
		int minimumDistance = 1000000; // store the minimum distance
		int categoryID = 0; // store song category ID's
		int categoryNumbers = 0;
		int[] songDistanceValues = new int[10]; // this is used to store the distance a song is from a category

		String tokens = "";
		String badSongs = "";
		String errors;
		// while the file has a next line
		while (inFile.hasNextLine()) {
			inLine = inFile.nextLine();
			// use string tokenizer to split each line by commas
			st = new StringTokenizer(inLine, ",");
			songID = st.nextToken(); // this takes the first token as the song ID/name and stores it in the variable

			for (col = 0; col < 7; col++) {
				try {
					tokens = st.nextToken();
					if (col >= 6) { // this code here will check if the elements after the songID are the correct
						// length
						badSongs = inLine + "Error, too many aspect values for this song";
						errorFile.println(badSongs);
						break;
					} else {
						songAspectValues[col] = Integer.parseInt(tokens); // parse the integers from the rest of the
						// line and store them here
					} // end if/else

				} // end try block
				catch (NumberFormatException e) {
					if (col == 0 & Character.isLetter(tokens.charAt(1))) {
						errors = inLine + "  (Error: There are unsupported characters in the song title)";
					} else {
						errors = inLine + "   (Error: there are non-integer characters on this line)";
						errorFile.println(errors);
						break;
					} // end if/else
				} // end catch block
				catch (NoSuchElementException e) {
					if (col < 5) {
						errors = inLine + "   (Error: there are not enough aspect values on this line)";
						errorFile.println(errors);
						break;
					} // end if
				} // end try/ multi-catch block

			} // end for loop
				//this block of code to is store and calculate the distance between each song category and song
			for (lineCount = 0; lineCount < numberofCategories; lineCount++) {
				distance = 0;
				for (col = 1; col < 7; col++) {
					// this code block here is calculating the distance between a songs aspect
					// values and all of the categories
					// using a nested loop to do this
					distance += (songAspectValues[col - 1] - songCategories[lineCount][col]) * (songAspectValues[col - 1] - songCategories[lineCount][col]);
					if (minimumDistance > distance) { // set minimum distance song to distance if minDistance is larger
						// than distance for that aspect
						minimumDistance = distance;
						categoryID = songCategories[lineCount][0];
						categoryNumbers = lineCount;
					} // end if
				} // end for

				song_categoryOutFile.println(songID + "   ( " + categoryID + " ) "); // output the songID and category
				// ID to the output file

				// place smallest distance and song ID for a category
				songDistanceValues[categoryNumbers] = minimumDistance;
				if (minSongDistance[categoryNumbers] > songDistanceValues[categoryNumbers]) {
					minSongDistance[categoryNumbers] = songDistanceValues[categoryNumbers];
					songsArray[categoryNumbers] = songID;
				} // end if statement

				songCategories[categoryNumbers][7] += 1; // calculate the number of songs that chose this category as
				// closest
			} // end for loop
		} // end while loop

		// this for loop will print out the category stats
		for (lineCount = 0; lineCount < numberofCategories; lineCount++) {
			outFile_CategoryStats.println(songCategories[lineCount][0] + "  ( " + songCategories[lineCount][7] + " )  " + songsArray[lineCount]);
		} // end for loop

		// close all input and output files
		inFile.close();
		errorFile.close();
		outFile_CategoryStats.close();
		song_categoryOutFile.close();

		System.out.println("Program finished");

	}// end main
} // end class
