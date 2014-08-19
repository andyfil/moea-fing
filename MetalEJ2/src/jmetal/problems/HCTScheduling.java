package jmetal.problems;

import java.io.BufferedWriter;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.Scanner;

import jmetal.core.Problem;
import jmetal.core.Solution;
import jmetal.encodings.solutionType.ArrayIntAndPermutationSolutionType;
import jmetal.encodings.variable.ArrayInt;
import jmetal.encodings.variable.Permutation;
import jmetal.util.JMException;

@SuppressWarnings("serial")
public class HCTScheduling extends Problem {

	private int cantidadTareas = 0;
	private int cantidadMaquinas = 0;
	// por ahora se supone 4 estados 100% 80% 60% 40%
	private int cantidadEstados = 0;// se supone que el estado más alto es el
									// más rapido y más consumidor de energía
	private long[][][] matriz_tiempo;// maquina_estado_tarea = militiempo
	private long[][] matriz_energia;// maquina_energia = energia/segundo
	private long[] matriz_energia_idle;// consumo de cada maquina en estado idle

	public HCTScheduling() {

	}

	// ------------------------------------------------------------------------------------------------------
	// TODO El constructor debería cambiar y dejar de tomar como parámetros la
	// cantidad de tareas, maquinas y estados
	public HCTScheduling(int cant_tareas, int cant_maquinas, int cant_estados)
			throws FileNotFoundException {

		numberOfVariables_ = 2;
		numberOfObjectives_ = 2;
		numberOfConstraints_ = 0;
		problemName_ = "HCTScheduling";

		upperLimit_ = new double[numberOfVariables_];
		lowerLimit_ = new double[numberOfVariables_];

		length_ = new int[numberOfVariables_];
		// variable 0 es la permutación de tareas
		lowerLimit_[0] = 0;
		upperLimit_[0] = cant_tareas + cant_maquinas - 1 - 1;
		length_[0] = cant_tareas + (cant_maquinas - 1); // se supone la
														// posición de
														// la primer
														// máquina
		// variable 1 es el estado en el que se ejecuta cada una de las tareas
		lowerLimit_[1] = 0;
		upperLimit_[1] = cant_estados - 1;
		length_[1] = cant_tareas;// un estado definido por cada tarea
		cantidadTareas = cant_tareas;
		cantidadMaquinas = cant_maquinas;
		cantidadEstados = cant_estados;
		matriz_tiempo = new long[cantidadMaquinas][cantidadEstados][cantidadTareas];
		matriz_energia = new long[cantidadMaquinas][cantidadEstados];
		matriz_energia_idle = new long[cantidadMaquinas];
		populateMatriz();
		// /*
		FileOutputStream fos;
		try {
			fos = new FileOutputStream("matriz tiempo");

			OutputStreamWriter osw = new OutputStreamWriter(fos);
			BufferedWriter bw = new BufferedWriter(osw);
			for (int maq = 0; maq < matriz_tiempo.length; maq++)
				for (int tar = 0; tar < cantidadTareas; tar++)
					for (int est = 0; est < cantidadEstados; est++)
						bw.write("m " + maq + " " + "t " + tar + " " + "e "
								+ est + " " + matriz_tiempo[maq][est][tar]
								+ "\n");
			bw.write("\n\nEnergía\n\n");
			for (int maq = 0; maq < cantidadMaquinas; maq++)
				for (int est = 0; est < cantidadEstados; est++)
					bw.write("m " + maq + " " + "e " + est + " "
							+ matriz_energia[maq][est] + "\n");
			bw.write("\n\nEnergía Idle\n\n");
			for (int maq = 0; maq < cantidadMaquinas; maq++)
				bw.write("m " + maq + " " + matriz_energia_idle[maq] + "\n");
			bw.close();
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

		catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		// */

		solutionType_ = new ArrayIntAndPermutationSolutionType(this);
	}

	@Override
	public void evaluate(Solution solution) throws JMException {
		Permutation tareas;// guarda las tareas codificadas del 0 a cantTareas
							// -1 y luego las maquinas como i- cantTareas
		ArrayInt estados; // contiene el estado en que se realiza cada tarea
		double makespan;
		double energy = 0;
		double[] energyNoIdle = new double[cantidadMaquinas];
		double[] tiempoNoIdle = new double[cantidadMaquinas];
		// maquina_tarea_estado: contiene estados para cada maquina
		ArrayList<LinkedList<TareaEstado>> maquina_tarea_estado = new ArrayList<LinkedList<TareaEstado>>(
				cantidadMaquinas);
		for (int i = 0; i < cantidadMaquinas; i++)
			maquina_tarea_estado.add(new LinkedList<TareaEstado>());// inicializo
																	// el array
																	// list
		estados = (ArrayInt) solution.getDecisionVariables()[0];
		tareas = (Permutation) solution.getDecisionVariables()[1];

		// First function calculo de energía
		int maqActual = 0;
		int j = 0;
		// recorro la permutación de tareas, y obtengo de la misma las tareas
		// que se ejecutan en cada maquina y en que estado
		for (int i = 0; i < tareas.getLength(); i++) {
			if (tareas.vector_[i] >= cantidadTareas) {
				maqActual = tareas.vector_[i] - cantidadTareas + 1;
			} else {
				maquina_tarea_estado.get(maqActual)
						.add(new TareaEstado(tareas.vector_[i], estados
								.getValue(j)));
				j++;
			}
		}
		// recorro la lista obtenida y quiero calcular cuanto tiempo consume en
		// cada maquina el ejecutar las tareas
		makespan = 0;
		for (int i = 0; i < cantidadMaquinas; i++) {
			double tiempoMaquina = 0;
			double energiaMaquina = 0;
			for (Iterator<TareaEstado> it = maquina_tarea_estado.get(i)
					.iterator(); it.hasNext();) {
				TareaEstado te = it.next();
				tiempoMaquina += matriz_tiempo[i][te.estado][te.tarea];// tiempo
																		// que
																		// lleva
																		// una
																		// tarea
																		// en un
																		// estado
																		// en
																		// una
																		// maquina
				energiaMaquina += matriz_tiempo[i][te.estado][te.tarea]
						* matriz_energia[i][te.estado] / 1000;// tiempo por
																// energia/tiempo
			}
			energyNoIdle[i] = energiaMaquina;
			tiempoNoIdle[i] = tiempoMaquina;
			makespan = Math.max(makespan, tiempoMaquina);// el maximo entre el
															// makespan anterior
															// y el de esta
															// maquina
		}
		for (int i = 0; i < cantidadMaquinas; i++) {
			energy += energyNoIdle[i] + (makespan - tiempoNoIdle[i])
					* matriz_energia_idle[i] / 1000;// el tiempo que quedo idle
													// por la energia y se suma
													// al total
		}

		solution.setObjective(0, makespan / 1000);
		solution.setObjective(1, energy / 1000);

	}

	private void populateMatriz() throws FileNotFoundException {

		// Leo del archivo que tiene cantidad de operaciones por tarea
		FileInputStream fis;
		fis = new FileInputStream("C:\\instancia");
		InputStreamReader isr = new InputStreamReader(fis);
		// BufferedReader br = new BufferedReader(isr);
		Scanner scan = new Scanner(isr);
		long ops;
		int i = 0;
		long[] op_por_tarea = new long[cantidadTareas];

		while (scan.hasNext() && i < cantidadTareas) {
			scan.next();
			scan.nextInt();
			scan.next();
			ops = scan.nextLong();
			op_por_tarea[i] = ops;
			i++;
		}
		scan.close();

		// Leo del archivo que tiene la matriz_idle_frec_consumo_operaciones por
		// maquinas
		FileInputStream fis2;
		fis2 = new FileInputStream("C:\\matriz_idle_frec_consumo_operaciones");
		InputStreamReader isr2 = new InputStreamReader(fis2);
		Scanner scan2 = new Scanner(isr2);
		long[] matriz_idle = new long[cantidadMaquinas];
		// double[] matriz_frec = new double[cantidadMaquinas];
		long[][] consumo = new long[cantidadMaquinas][cantidadEstados];
		long[][] operaciones = new long[cantidadMaquinas][cantidadEstados];

		double energia_idle, frecuencia_maq, consumo_maq;
		long operaciones_maq;
		int maq;
		while (scan2.hasNext()) {
			maq = scan2.nextInt();
			energia_idle = scan2.nextDouble();
			frecuencia_maq = scan2.nextDouble();
			matriz_idle[maq - 1] = (long) energia_idle;
			// matriz_frec[maq-1] = frecuencia_maq;
			for (int est = 0; est < cantidadEstados; est++) {
				consumo_maq = scan2.nextDouble();
				consumo[maq - 1][est] = (long) consumo_maq;
				operaciones_maq = scan2.nextLong();
				operaciones[maq - 1][est] = (long) operaciones_maq;
			}
		}
		scan2.close();

		/********************* PRUEBO QUE CARGUE BIEN OPERACIONES POR TAREA ***********************/
		// FileOutputStream fos;
		// try {
		// fos = new FileOutputStream("operaciones por tarea");
		//
		// OutputStreamWriter osw = new OutputStreamWriter(fos) ;
		// BufferedWriter bw = new BufferedWriter(osw) ;
		// for(int j=0; j < ops_por_tarea.length; j++)
		// bw.write("tarea  " + j + " " + "ops "+ ops_por_tarea[j] + "\n");
		// bw.close();
		// } catch (FileNotFoundException e) {
		// // TODO Auto-generated catch block
		// e.printStackTrace();
		// }
		//
		// catch (IOException e) {
		// // TODO Auto-generated catch block
		// e.printStackTrace();
		// }
		/******************************************************************************************/
		/********************* PRUEBO QUE CARGUE BIEN MATRIZ_IDLE_FREC_CONSUMO_OPERACIONES ***********************/
		// FileOutputStream fos2;
		// try {
		// fos2 = new
		// FileOutputStream("matriz idle frec consumo operaciones por maquina");
		//
		// OutputStreamWriter osw2 = new OutputStreamWriter(fos2) ;
		// BufferedWriter bw2 = new BufferedWriter(osw2) ;
		// for(int j=1; j <= matriz_idle.length; j++){
		// bw2.write(j + " " + matriz_idle[j-1] + " " + matriz_frec[j-1] + " " +
		// consumo[j-1] + " " + operaciones[j-1] + "\n");
		// }
		// bw2.close();
		// } catch (FileNotFoundException e) {
		// // TODO Auto-generated catch block
		// e.printStackTrace();
		// }
		//
		// catch (IOException e) {
		// // TODO Auto-generated catch block
		// e.printStackTrace();
		// }
		/******************************************************************************************/

		double factor = 0;
		long ops_estado;
		for (int m = 0; m < cantidadMaquinas; m++) {

			matriz_energia_idle[m] = matriz_idle[m];

			for (int e = 0; e < cantidadEstados; e++) {
				matriz_energia[m][e] = consumo[m][e];

				for (int t = 0; t < cantidadTareas; t++) {
					ops_estado = operaciones[m][e];
					matriz_tiempo[m][e][t] = op_por_tarea[t] / ops_estado;

				}
			}
		}
	}

	private class TareaEstado {
		public TareaEstado(int p_tarea, int p_estado) {
			tarea = p_tarea;
			estado = p_estado;
		}

		public int tarea;
		public int estado;
	}
}
