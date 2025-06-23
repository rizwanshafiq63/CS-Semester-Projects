import java.util.ArrayList;
import java.util.Collections;

public class DivingScoreLogic {
    public static double calculateFinalScore(ArrayList<Double> scores, double difficulty) {
        if (scores.size() != 7) throw new IllegalArgumentException("Exactly 7 scores required.");
        if (difficulty < 1.2 || difficulty > 3.8) throw new IllegalArgumentException("Invalid difficulty.");

        double max = Collections.max(scores);
        double min = Collections.min(scores);

        scores.remove(max);
        scores.remove(min);

        double sum = 0;
        for (double score : scores) {
            sum += score;
        }

        return sum * difficulty * 0.6;
    }
}

public class 04_new {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        ArrayList<Double> scores = new ArrayList<>();

        double difficulty;
        while (true) {
            System.out.print("Enter difficulty (1.2 to 3.8): ");
            difficulty = scanner.nextDouble();
            if (difficulty >= 1.2 && difficulty <= 3.8) break;
            System.out.println("Invalid. Try again.");
        }

        System.out.println("Enter 7 scores (0 to 10):");
        while (scores.size() < 7) {
            double s = scanner.nextDouble();
            if (s >= 0 && s <= 10) {
                scores.add(s);
            } else {
                System.out.println("Invalid score. Try again.");
            }
        }

        double result = DivingScoreLogic.calculateFinalScore(new ArrayList<>(scores), difficulty);
        System.out.printf("Final diving score: %.2f\n", result);
    }
}

