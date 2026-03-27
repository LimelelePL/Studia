
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.Locale;

import core.AbstractSwappingSortingAlgorithm;
import testing.*;
import testing.comparators.*;
import testing.generation.*;
import testing.generation.conversion.*;
import testing.results.swapping.Result;

public class Main {

	public static void main(String[] args) {
		Locale.setDefault(Locale.US);
		Comparator<MarkedValue<Integer>> markedComparator = new MarkedValueComparator<Integer>(new IntegerComparator());

		AbstractSwappingSortingAlgorithm<MarkedValue<Integer>> selectionSort = new SelectionSort<>(markedComparator);
		AbstractSwappingSortingAlgorithm<MarkedValue<Integer>> coctailSort = new CoctailSort<>(markedComparator);
		AbstractSwappingSortingAlgorithm<MarkedValue<Integer>> insertionSort = new InsertionSort<>(markedComparator);

		ArrayList<AbstractSwappingSortingAlgorithm<MarkedValue<Integer>>> algorytmy= new ArrayList<>();
		algorytmy.add(selectionSort);
		algorytmy.add(coctailSort);
		algorytmy.add(insertionSort);

        Generator<MarkedValue<Integer>> [] generators = new Generator[4];
		generators[0] = new MarkingGenerator<Integer>(new RandomIntegerArrayGenerator(10));
		generators[1] = new MarkingGenerator<Integer>(new OrderedIntegerArrayGenerator());
		generators[2]= new MarkingGenerator<Integer>(new ReversedIntegerArrayGenerator());
		generators[3]= new MarkingGenerator<Integer>(new ShuffledIntegerArrayGenerator(10));
		String[] generatorNames = {"random","ordered", "reversed", "shuffled"};

		String[] algorithmNames = {
				"selectionSort", "coctailSort", "insertionSort"
		};

		int[] sizes = {0,5,10,20,30,40,50,75,100, 150, 200, 250,500,1000,2000, 5000,10000};

		try (PrintWriter out = new PrintWriter(new FileWriter("results.csv"))) {

			out.println("algorithm,inputType,size,avgTime,stdTime,avgCmp,stdCmp,avgSwap,stdSwap,sorted,stable");

			for (int a=0; a<algorytmy.size(); a++) {

				AbstractSwappingSortingAlgorithm<MarkedValue<Integer>> algorithm = algorytmy.get(a);
				String algorithmName = algorithmNames[a];

				for (int g = 0; g < generators.length; g++) {
					Generator<MarkedValue<Integer>> gen = generators[g];
					String inputType = generatorNames[g];

					for (int size : sizes) {
						try {
							System.out.printf("Running: %s / %s / size = %d\n", algorithmName, inputType, size);
							Result result = Tester.runNTimes(algorithm, gen, size, 20);
							writeToCSV(result, algorithmName, inputType, size, out);
						} catch (Exception e) {
							System.err.printf("Błąd przy %s / %s / size=%d: %s\n", algorithmName, inputType, size, e.getMessage());
						}
					}
				}
			}

		} catch (IOException e) {
			e.printStackTrace();
		}

	}
	public static void printInConsole(testing.results.swapping.Result algoritmResult, String algoritmName){
		System.out.println("-------------" + algoritmName.toUpperCase() + "-------------");
		printStatistic("time [ms]", algoritmResult.averageTimeInMilliseconds(), algoritmResult.timeStandardDeviation());
		printStatistic("comparisons", algoritmResult.averageComparisons(), algoritmResult.comparisonsStandardDeviation());
		printStatistic("swaps", algoritmResult.averageSwaps(), algoritmResult.swapsStandardDeviation());

		System.out.println("always sorted: " + algoritmResult.sorted());
		System.out.println("always stable: " + algoritmResult.stable());
	}
	
	private static void printStatistic(String label, double average, double stdDev) {
		System.out.println(label + ": " + double2String(average) + " +- " + double2String(stdDev));
	}
	
	private static String double2String(double value) {
		return String.format("%.12f", value);
	}

	public static void writeToCSV(Result result, String algorithmName, String inputType, int size, PrintWriter out) {
		out.printf("%s,%s,%d,%.6f,%.6f,%.0f,%.6f,%.0f,%.6f,%s,%s\n",
				algorithmName,
				inputType,
				size,
				result.averageTimeInMilliseconds(),
				result.timeStandardDeviation(),
				result.averageComparisons(),
				result.comparisonsStandardDeviation(),
				result.averageSwaps(),
				result.swapsStandardDeviation(),
				result.sorted(),
				result.stable()
		);
	}
}
