/* In the sport of diving, seven judges award a score between 0 and 10, where each score may be a floating-point value. The highest and lowest scores are thrown out and the remaining scores are added together. The sum is then multiplied by the degree of difficulty for that dive. The degree of difficulty ranges from 1.2 to 3.8 points. The total is then multiplied by 0.6 to determine the diver’s score.
Write a computer program that inputs a degree of difficulty and seven judges’ scores and outputs the overall score for that dive. The program should use an ArrayList of type Double to store the scores. */

import java.util.ArrayList;
import java.util.Collections;
import java.util.Scanner;

public class Lab10_Task_04 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        ArrayList<Double> scores = new ArrayList<>();

        // Input: Degree of difficulty
        double difficulty;
        while (true) {
            System.out.print("Enter the degree of difficulty (1.2 to 3.8): ");
            difficulty = scanner.nextDouble();
            if (difficulty >= 1.2 && difficulty <= 3.8) {
                break;
            } else {
                System.out.println("Invalid input. Please enter a value between 1.2 and 3.8.");
            }
        }

        // Input: 7 judges' scores
        System.out.println("Enter 7 judges’ scores (between 0 and 10):");
        int count = 0;
        while (count < 7) {
            System.out.print("Score " + (count + 1) + ": ");
            double score = scanner.nextDouble();
            if (score >= 0 && score <= 10) {
                scores.add(score);
                count++;
            } else {
                System.out.println("Invalid score. Please enter a value between 0 and 10.");
            }
        }

        // Remove highest and lowest score
        double max = Collections.max(scores);
        double min = Collections.min(scores);
        scores.remove(max);
        scores.remove(min);

        // Calculate sum of remaining scores
        double total = 0;
        for (double score : scores) {
            total += score;
        }

        // Calculate final score
        double finalScore = total * difficulty * 0.6;

        System.out.printf("Final diving score: %.2f\n", finalScore);
    }
}



