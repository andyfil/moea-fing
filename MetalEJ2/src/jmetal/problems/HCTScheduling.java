package jmetal.problems;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.LinkedList;

import jmetal.core.Problem;
import jmetal.core.Solution;
import jmetal.encodings.solutionType.ArrayIntAndPermutationSolutionType;
import jmetal.encodings.variable.ArrayInt;
import jmetal.encodings.variable.Permutation;
import jmetal.util.JMException;

public class HCTScheduling extends Problem {

	private int cantidadTareas = 0;
	private int cantidadMaquinas = 0;
	//por ahora se supone 4 estados 100% 80% 60% 40% 
	private int cantidadEstados = 0;// se supone que el estado más alto es el
									// más rapido y más consumidor de energía
	private double[][][] matriz_tiempo;// maquina_estado_tarea = militiempo
	private double[][] matriz_energia;// maquina_energia = energia/segundo 
	private double[] matriz_energia_idle;// consumo de cada maquina en estado idle

	public HCTScheduling (){
	
	}
	public HCTScheduling(int cant_tareas,
			int cant_maquinas, int cant_estados) {

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
		upperLimit_[1] = cant_estados -1;
		length_[1] = cant_tareas;// un estado definido por cada tarea
		cantidadTareas = cant_tareas;
		cantidadMaquinas = cant_maquinas;
		cantidadEstados = cant_estados;
		matriz_tiempo = new double[cantidadMaquinas][cantidadEstados][cantidadTareas];
		matriz_energia = new double[cantidadMaquinas][cantidadEstados];
		matriz_energia_idle = new double[cantidadMaquinas];
		populateMatriz();
		solutionType_ = new ArrayIntAndPermutationSolutionType(this);
	}

	@Override
	public void evaluate(Solution solution) throws JMException {
		Permutation tareas;// guarda las tareas codificadas del 0 a cantTareas -1 y luego las maquinas como i- cantTareas
		ArrayInt estados;
		double makespan; 
		double energy=0;
		double [] energyNoIdle = new double [cantidadMaquinas];
		double [] tiempoNoIdle = new double [cantidadMaquinas];
		ArrayList<LinkedList<TareaEstado>> maquina_tarea_estado = new ArrayList<LinkedList<TareaEstado>>(cantidadMaquinas);
		for(int i = 0;i<cantidadMaquinas;i++) maquina_tarea_estado.add(new LinkedList<TareaEstado>());//inicializo el array list
		tareas= (Permutation) solution.getDecisionVariables()[0];
		estados= (ArrayInt) solution.getDecisionVariables()[1];

		// First function calculo de energía
		int maqActual = 0;
		int j = 0;
		//recorro la permutación de tareas, y obtengo de la misma las tareas que se ejecutan en cada maquina y en que estado
		for(int i = 0; i < tareas.getLength();i++){
			if (tareas.vector_[i]>=cantidadTareas){
				maqActual =tareas.vector_[i] - cantidadTareas + 1; 
			}else{
					maquina_tarea_estado.get(maqActual).add(new TareaEstado(tareas.vector_[i],estados.getValue(j)));
			}
		}
		//recorro la lista obtenida y quiero calcular cuanto tiempo consume en cada maquina el ejecutar las tareas
		makespan =0;
		for (int i=0;i<cantidadMaquinas;i++){
			double tiempoMaquina = 0;
			double energiaMaquina = 0;
			for (Iterator<TareaEstado> it = maquina_tarea_estado.get(i).iterator();it.hasNext();){
				TareaEstado te = it.next();
				tiempoMaquina += matriz_tiempo[i][te.estado][te.tarea];//tiempo que lleva una tarea en un estado en una maquina
				energiaMaquina += matriz_tiempo[i][te.estado][te.tarea] * matriz_energia[i][te.estado]/1000;//tiempo por energia/tiempo
			}
			energyNoIdle[i]=energiaMaquina;
			tiempoNoIdle[i]=tiempoMaquina;
			makespan = Math.max(makespan, tiempoMaquina);//el maximo entre el makespan anterior y el de esta maquina
		}
		for(int i=0;i<cantidadMaquinas;i++){
			energy +=energyNoIdle[i]+ (tiempoNoIdle[i] - makespan) * matriz_energia_idle[i]/1000;//el tiempo que quedo idle por la energia y se suma al total
		}
		
		solution.setObjective(0, makespan);
		solution.setObjective(1, energy);

	}

	private void populateMatriz() {
		double [] tiempoBaseTarea = new double[cantidadTareas];
		double [] freqPerState = new double [cantidadEstados];
		double freqBase = 0.4;
		for(int e = 0; e < cantidadEstados;e++){
			freqPerState[e] = freqBase + (e*0.2); 
		}
		for (int t = 0; t<cantidadTareas;t++){
			tiempoBaseTarea[t]=10000 + (Math.random() * 50000) ;
		}
		for (int m = 0; m < cantidadMaquinas; m++) {
			double boostMaquina = Math.random() / 2; 		// define el boost que brinda la maquina seleccionada en tiempo
			double energiaBaseMaq = 140 + (Math.random()*(30)); 						// energía base por unidad de tiempo
			double timeBoostForFrecuency =0.05 + (Math.random() * (0.07));
			
			matriz_energia_idle[m] = Math.round(25*(1- boostMaquina));
			
			for (int e = 0; e < cantidadEstados; e++) {
				double timeBoost = timeBoostForFrecuency* (1 - freqPerState[e]/freqBase);
								
				matriz_energia[m][e] = energiaBaseMaq * freqPerState[e];
				
				for (int t = 0; t < cantidadTareas; t++) {
					matriz_tiempo[m][e][t] = tiempoBaseTarea[t] * (1 - timeBoost);

				}
			}
		}
	}

	// Esto es para usar luego, una vez que tengamos medio dominado el tema del
	// problema comenzamos a leer los datos que definen la instancia de un
	// archivo
	public void readProblem(String fileName) throws IOException {
		// Reader inputFile = new BufferedReader(new InputStreamReader(
		// new FileInputStream(fileName)));
		//
		// StreamTokenizer token = new StreamTokenizer(inputFile);
		// try {
		// boolean found;
		// found = false;
		//
		// token.nextToken();
		// for(int )
		// numberOfCities_ = (int) token.nval;
		//
		// distanceMatrix_ = new double[numberOfCities_][numberOfCities_];
		//
		// // Find the string SECTION
		// found = false;
		// token.nextToken();
		// while (!found) {
		// if ((token.sval != null)
		// && ((token.sval.compareTo("SECTION") == 0)))
		// found = true;
		// else
		// token.nextToken();
		// } // while
		//
		// // Read the data
		//
		// double[] c = new double[2 * numberOfCities_];
		//
		// for (int i = 0; i < numberOfCities_; i++) {
		// token.nextToken();
		// int j = (int) token.nval;
		//
		// token.nextToken();
		// c[2 * (j - 1)] = token.nval;
		// token.nextToken();
		// c[2 * (j - 1) + 1] = token.nval;
		// } // for
		//
		// double dist;
		// for (int k = 0; k < numberOfCities_; k++) {
		// distanceMatrix_[k][k] = 0;
		// for (int j = k + 1; j < numberOfCities_; j++) {
		// dist = Math.sqrt(Math.pow((c[k * 2] - c[j * 2]), 2.0)
		// + Math.pow((c[k * 2 + 1] - c[j * 2 + 1]), 2));
		// dist = (int) (dist + .5);
		// distanceMatrix_[k][j] = dist;
		// distanceMatrix_[j][k] = dist;
		// } // for
		// } // for
		// } // try
		// catch (Exception e) {
		// System.err
		// .println("TSP.readProblem(): error when reading data file "
		// + e);
		// System.exit(1);
		// } // catch
	} // readProblem

	private class TareaEstado{
		public TareaEstado(int p_tarea, int p_estado){
			tarea =p_tarea;
			estado= p_estado;
		}
		public int tarea;
		public int estado;
	}
}
