package estudioParametrico;

import java.io.BufferedWriter;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.Arrays;
import java.util.Scanner;

public class estudiar {

	private static int [] index_orders;	
	
	public static void main(String[] args) throws FileNotFoundException {
		int cantAlgoritmos = 9;
		int cantEjecuciones = 20;
		double [] mejorM_alg = new double [cantAlgoritmos];
		double [] mejorE_alg = new double [cantAlgoritmos];
		for (int l=0; l<cantAlgoritmos; l++)
			mejorM_alg[l] = 1000000;
	    for (int k=0; k<cantAlgoritmos; k++)
			mejorE_alg[k] = 1000000;
	    double [] mejorI_alg = new double [cantAlgoritmos];
		double [] promedioI_alg = new double [cantAlgoritmos];
		double [] peorI_alg = new double [cantAlgoritmos];
		int [] sol_alg = new int [cantAlgoritmos];
		double [] promedio_compromiso = new double [cantAlgoritmos];
		double total_distancias = 0;
		int cant_soluciones = 0;
		for (int l=0; l<cantAlgoritmos; l++)
			mejorI_alg[l] = 100000;
	    for (int m=0; m<cantAlgoritmos; m++)
	    	peorI_alg[m] = 1;
	    
	    // Leo de archivo el frente de pareto de referencia: "HCTScheduling.rf"
		FileInputStream fisRF;
		fisRF = new FileInputStream("C:\\HCTEstudio\\referenceFronts\\HCTScheduling.rf");
		InputStreamReader isrRF = new InputStreamReader(fisRF);
	    Scanner scanRF = new Scanner(isrRF);
	    int iRF = 0;
	    float makespanRF;
	    float energyRF;
	    float [][] paretoRF = new float[1000][2]; // Array con el frente de pareto real de todas las ejecuciones
	    while (scanRF.hasNext()){
	    	String tokenRF = scanRF.next();
	    	makespanRF = Float.parseFloat(tokenRF);
	    	
	    	tokenRF = scanRF.next();
	    	energyRF = (float) Double.parseDouble(tokenRF);
	    	
	    	paretoRF[iRF][0] = makespanRF;
	    	paretoRF[iRF][1] = energyRF;
	    		    	
	    	iRF++;
	    }
	    scanRF.close();
	    int [] soluciones_en_rf = new int [cantEjecuciones];
	    for (int z=0; z<cantEjecuciones; z++)
	    	soluciones_en_rf[z] = 0;
	    
		FileOutputStream fos;
		try {
			fos = new FileOutputStream("C:\\HCTEstudio\\estudio");
			OutputStreamWriter osw = new OutputStreamWriter(fos)    ;
			BufferedWriter bw      = new BufferedWriter(osw); 
		    
			// Busco el mejor valor, promedio y peor de cada ejecucion para cada algoritmo	
			String numAlg = "";
			for (int i = 0; i < cantAlgoritmos; i++){
				double [] iteraciones_alg = new double [20];
				numAlg = Integer.toString(i);
				String alg = "NSGAII";
				alg = alg.concat(numAlg);
				System.out.println("****Algoritmo " + alg + "****");
				bw.write("****Algoritmo " + alg + "****\n");
				
				// Busco el mejor valor, promedio y peor de cada ejecucion para un algoritmo
				// Busco el mejor valor, promedio y peor de iteraciones necesarias para un algoritmo
				String numEjec = "";
				for (int j = 0; j < cantEjecuciones; j++){
					// Busco el mejor valor, promedio y peor de la ejecucion = cantEjecuciones
					FileInputStream fis;
					// Armo la ejecucion a leer de archivo
					numEjec = Integer.toString(j);
					String ejec = "FUN.";
					ejec = ejec.concat(numEjec);
					fis = new FileInputStream("C:\\HCTEstudio\\data\\" + alg + "\\HCTScheduling\\" + ejec);
					InputStreamReader isr = new InputStreamReader(fis); 
				    Scanner scan = new Scanner(isr);
				    long makespan;
				    float energy;
				    double mejorM = Double.MAX_VALUE;
				    float mejorE = Float.MAX_VALUE;
				    double acumuladorM = 0;
				    float acumuladorE = 0;
				    double peorM = 0;
				    float peorE = 0;
				    int cantidad = 0;
				    long menor_distancia = Long.MAX_VALUE;
				    long distancia = 0;
				    double res = 0;
				    double sol_comp_x = 0;
				    double sol_comp_y = 0;
				    double x = 0;
				    double y = 0;
				    soluciones_en_rf[j] = 0;
				    
				    while (scan.hasNext()){
				    	String token = scan.next();
				    	makespan = (long) Double.parseDouble(token);
				    	acumuladorM += makespan;
				    	if (makespan < mejorM)
				    		mejorM = makespan;
				    	if (makespan > peorM)
				    		peorM = makespan;
				    	
				    	token = scan.next();
				    	energy = (float) Float.parseFloat(token);
				    	acumuladorE += energy;
				    	if (energy < mejorE)
				    		mejorE = energy;
				    	if (energy > peorE)
				    		peorE = energy;
				    	
				    	res = Math.pow(makespan-x,2) + Math.pow(energy-y, 2);
				    	distancia = (long) Math.sqrt(res);
				    	System.out.println("Ejecucion: " + ejec + ", distancia : " + distancia);
				    	
				    	// Pregunto si es mejor distancia
				    	if (distancia < menor_distancia){
				    		menor_distancia = distancia;
				    		sol_comp_x = makespan;
				    		sol_comp_y = energy;
				    	}
				    	// Pregunto si esta solucion pertenece al frente de pareto real de referencia
				    	for (int aux=0; aux<iRF; aux++){
				    		if (makespan==paretoRF[aux][0] && energy==paretoRF[aux][1]){
				    			soluciones_en_rf[j]++;
				    			cant_soluciones++;
				    			break;
				    		}
				    	}
				    	
				    	cantidad++;
				    }
				    System.out.println("Menor distancia : " + menor_distancia);
				    double promedioM = acumuladorM / cantidad;
				    float promedioE = acumuladorE / cantidad;
				    // Promedio de distancia de soluciones de compromiso
				    total_distancias += menor_distancia;
				    
				    // Busco el mejor valor de cada algoritmo
				    if (mejorE < mejorE_alg[i])
				    	mejorE_alg[i] = mejorE;
				    if (mejorM < mejorM_alg[i])
				    	mejorM_alg[i] = mejorM;
				    
				    iteraciones_alg[j] = cantidad;
				    // Busco la mejor cantidad de iteraciones de cada algoritmo
				    if (cantidad < mejorI_alg[i])
				    	mejorI_alg[i] = cantidad;
				    if (cantidad > peorI_alg[i])
				    	peorI_alg[i] = cantidad;
				    
				    // Escrbo en el archivo	
					bw.write(ejec + ":\n");
					//bw.write("Mejor makespan: " + mejorM + "\n");
					//bw.write("Mejor energy: " + mejorE + "\n");
					//bw.write("Promedio makespan " + promedioM + "\n");
					//bw.write("Promedio energy " + promedioE + "\n");
					//bw.write("Peor makespan " + peorM + "\n");
					//bw.write("Peor energy " + peorE + "\n");
					//bw.write("Mejor cantidad de iteraciones " + mejorI_alg[i] + "\n");
					//bw.write("Promedio cantidad de iteraciones " + promedioI_alg[i] + "\n");
					//bw.write("Peor cantidad de iteraciones " + peorI_alg[i] + "\n");
					bw.write("Solucion de compromiso (" + sol_comp_x + "," + sol_comp_y + "), distancia: " + menor_distancia + "\n");
					bw.write("Cantidad de soluciones en Frente de Pareto de Referencia: " + soluciones_en_rf[j] );
					bw.write("\n");
					
/*					// Salida a consola
					System.out.println(ejec + ":");
				    System.out.println("Mejor makespan: " + mejorM);
				    System.out.println("Mejor energy: " + mejorE);*/
				    System.out.println("Promedio makespan " + promedioM);
				    System.out.println("Promedio energy " + promedioE);
				  /*  System.out.println("Peor makespan " + peorM);
				    System.out.println("Peor energy " + peorE);
				    System.out.println("Mejor cantidad de iteraciones " + mejorI_alg[i]);
				    System.out.println("Promedio cantidad de iteraciones " + promedioI_alg[i]);
				    System.out.println("Peor cantidad de iteraciones " + peorI_alg[i]);
				    System.out.println(" ");
*/
				    
				    scan.close();
				    
				} // END FOR para ejecuciones
				int totalI = 0;
				for (int fun=0; fun<cantEjecuciones; fun++){
					totalI += iteraciones_alg[fun];
				}
				promedioI_alg[i] = totalI/cantEjecuciones;
				sol_alg[i] = cant_soluciones;
				promedio_compromiso[i] = total_distancias/cantEjecuciones;
				bw.write("Cantidad de soluciones del FP en el algoritmo: " + cant_soluciones);
				bw.write("\n");
				bw.write("Distancia promedio de soluciones compromiso: " + promedio_compromiso[i]);
				bw.write("\n");
				bw.write("\n");
				cant_soluciones = 0;
				total_distancias = 0;
			} // END FOR para algoritmos
			 
			bw.close();
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}	
		
/*		
		// Creo y armo el archivo con los mejores valores de fitness por algoritmo
		FileOutputStream fos1;
		try {
			fos1 = new FileOutputStream("C:\\HTCEstudio\\fitness por algoritmo");
			OutputStreamWriter osw1 = new OutputStreamWriter(fos1);
			BufferedWriter bw1      = new BufferedWriter(osw1);
			String numAlg = ""; 
			for (int a = 0; a < cantAlgoritmos; a++){
				String alg = "NSGAII";
				numAlg = Integer.toString(a);
				alg = alg.concat(numAlg);
				bw1.write(alg + "\n");
				bw1.write("Mejor makespan: ");
				bw1.write(mejorM_alg[a] + " ");
				bw1.write("Mejor energy: ");
				bw1.write(mejorE_alg[4] + "\n");
//				bw1.write("Mejor cantidad de iteraciones: " + mejorI_alg[a]);
//				bw1.write(" ");
//				bw1.write("Promedio cantidad de iteraciones: " + promedioI_alg[a]);
//				bw1.write(" ");
//				bw1.write("Peor cantidad de iteraciones: " + peorI_alg[a] + "\n");
			}
			
			bw1.close();
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
*/		
		// Creo y armo el archivo con los mejores algoritmos ordenados por puntos ND en FP real de referencia
		int [] auxiliarND = new int [cantAlgoritmos];
		for (int aux=0; aux<cantAlgoritmos; aux++){
			auxiliarND[aux] = sol_alg[aux];
		}
		Arrays.sort(auxiliarND);
		int [] resND = invertIntArray(auxiliarND);
		index_orders = orderIntIndex(sol_alg, auxiliarND);
		FileOutputStream fosND;
		try {
			fosND = new FileOutputStream("C:\\HCTEstudio\\Orden Alg por #ND en FPrf");
			OutputStreamWriter oswND = new OutputStreamWriter(fosND);
			BufferedWriter bwND      = new BufferedWriter(oswND);
			String numAlg = ""; 
			for (int i = 0; i < cantAlgoritmos; i++){
				String alg = "NSGAII";
				numAlg = Integer.toString(index_orders[i]);
				alg = alg.concat(numAlg);
				bwND.write(alg + " ");
				bwND.write("#ND en FP de referencia: " + resND[i]);
				bwND.write("\n");
			}
			
			bwND.close();
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		// Creo y armo el archivo con los mejores algoritmos ordenados por distancia de soluciones de compromiso
		double [] auxiliarSC = new double [cantAlgoritmos];
		for (int aux=0; aux<cantAlgoritmos; aux++){
			auxiliarSC[aux] = promedio_compromiso[aux];
		}
		Arrays.sort(auxiliarSC);
		index_orders = orderDoubleIndex(promedio_compromiso, auxiliarSC);
		FileOutputStream fosSC;
		try {
			fosSC = new FileOutputStream("C:\\HCTEstudio\\Orden Alg por distancia SC");
			OutputStreamWriter oswSC = new OutputStreamWriter(fosSC);
			BufferedWriter bwSC      = new BufferedWriter(oswSC);
			String numAlg = ""; 
			for (int i = 0; i < cantAlgoritmos; i++){
				String alg = "NSGAII";
				numAlg = Integer.toString(index_orders[i]);
				alg = alg.concat(numAlg);
				bwSC.write(alg + " ");
				bwSC.write("Distancia promedio a Solucion de Compromiso: " + auxiliarSC[i]);
				bwSC.write("\n");
			}
			
			bwSC.close();
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		//NSGAII1, run: 0 -> Tiempo de inicio : 1408485191622
		//NSGAII3, run: 0 -> Tiempo de fin : 6911
		FileInputStream fist;
		fist = new FileInputStream("C:\\HCTEstudio\\tiempos_de_ejecuciones");
		InputStreamReader isrt = new InputStreamReader(fist);
		Scanner scant = new Scanner(isrt);
		String token, token_if = "";
		double tiempo_fin = 0;
		int num_alg = 0;
		double[][] matriz_tiempos = new double[cantAlgoritmos][cantEjecuciones];
		while (scant.hasNext()) {
			token = scant.next(); // Leo "NSGAIIi"
			num_alg = (int) token.charAt(6) - 48;
			token = scant.next(); // Leo "run:"
			int num_run = scant.nextInt();
			token = scant.next(); // Leo "->" 
			token = scant.next(); // Leo "Tiempo"
			token = scant.next(); // Leo "de"
			token_if = scant.next(); // Leo "inicio o fin"
			token = scant.next(); // Leo ":"
			// Pregunto si es tiempo de fin
			if (token_if.startsWith("f")){
				tiempo_fin = scant.nextDouble();
				matriz_tiempos[num_alg][num_run] = tiempo_fin;
			}
			else
				token = scant.next();
			
		}
		scant.close();
		imprimirTiempoDeFinPorAlgPorEjec(matriz_tiempos, cantAlgoritmos, cantEjecuciones);
		double [][] auxiliar_tiempos = new double [cantAlgoritmos][cantEjecuciones];
		// Tiempos por algoritmos
		double [] totales_tiempos = new double [cantAlgoritmos];
		double [] totales_tiempos_auxiliar = new double [cantAlgoritmos];
		double total_alg = 0;
		for (int aux=0; aux<cantAlgoritmos; aux++){
			for (int aux1=0; aux1<cantEjecuciones; aux1++){
				total_alg += matriz_tiempos[aux][aux1];
				auxiliar_tiempos[aux][aux1] = matriz_tiempos[aux][aux1];
			}
			totales_tiempos[aux] = total_alg;
			totales_tiempos_auxiliar[aux] = total_alg;
			total_alg = 0;
		}
		Arrays.sort(totales_tiempos_auxiliar);
		index_orders = orderDoubleIndex(totales_tiempos, totales_tiempos_auxiliar);
		for (int i=0; i<cantAlgoritmos; i++)
			System.out.println(index_orders[i]);
		FileOutputStream fost;
		try {
			fost = new FileOutputStream("C:\\HCTEstudio\\Orden Alg por tiempo");
			OutputStreamWriter oswt = new OutputStreamWriter(fost);
			BufferedWriter bwt      = new BufferedWriter(oswt);
			String numAlg = ""; 
			for (int i = 0; i < cantAlgoritmos; i++){
				String alg = "NSGAII";
				numAlg = Integer.toString(index_orders[i]);
				alg = alg.concat(numAlg);
				bwt.write(alg + " ");
				bwt.write("Tiempo total de ejecuciones: " + totales_tiempos_auxiliar[i]);
				bwt.write("\n");
			}
			
			bwt.close();
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
	} // main

	private static void imprimirTiempoDeFinPorAlgPorEjec(
			double[][] matriz_tiempos, int cantAlgoritmos, int cantEjecuciones) {
		FileOutputStream fosMT;
		try {
			fosMT = new FileOutputStream("C:\\HCTEstudio\\Tiempos Fin ALG x EJEC");
			OutputStreamWriter oswMT = new OutputStreamWriter(fosMT);
			BufferedWriter bwMT      = new BufferedWriter(oswMT);
			String numAlg = ""; 
			for (int i = 0; i < cantAlgoritmos; i++){
				String alg = "NSGAII";
				numAlg = Integer.toString(i);
				alg = alg.concat(numAlg);
				bwMT.write("****Algoritmo " + alg + "****\n");
				for (int j = 0; j < cantEjecuciones; j++) 
					
					/*bwMT.write("Tiempo de duracion de ejecucion " + j + " : " +*/bwMT.write(matriz_tiempos[i][j] + "\n");
					//bwMT.write("\n");
			}
			
			bwMT.close();
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
	}

	@SuppressWarnings("unused")
	private static double[] invertDoubleArray(double[] array) {
		int i = 0;
		int j = array.length - 1;
		double tmp;
		while (j > i) {
			tmp = array[j];
			array[j] = array[i];
			array[i] = tmp;
			j--;
			i++;
		}
		return array;
	}

	public static int[] invertIntArray(int[] array) {
		int i = 0;
		int j = array.length - 1;
		int tmp;
		while (j > i) {
			tmp = array[j];
			array[j] = array[i];
			array[i] = tmp;
			j--;
			i++;
		}
		return array;
	}
	
	private static int[] orderIntIndex(int[] disorderArray, int[] orderArray) {
		int lon = disorderArray.length;

		int[] index = new int[lon];
		Arrays.fill(index, 0);

		boolean[] esta = new boolean[lon];
		Arrays.fill(esta, false);

		for (int i = 0; i < orderArray.length; i++) {
			int in = 0;
			boolean stay = false;
			while (in < orderArray.length & !stay) {
				if ((disorderArray[in] == orderArray[i]) & !esta[in]) {
					esta[in] = true;
					index[i] = in;
					stay = true;
				} else {
					in++;
				}
			}
		}
		return index;
	}
	
	private static int[] orderDoubleIndex(double[] disorderArray, double[] orderArray) {
		int lon = disorderArray.length;

		int[] index = new int[lon];
		Arrays.fill(index, 0);

		boolean[] esta = new boolean[lon];
		Arrays.fill(esta, false);

		for (int i = 0; i < orderArray.length; i++) {
			int in = 0;
			boolean stay = false;
			while (in < orderArray.length & !stay) {
				if ((disorderArray[in] == orderArray[i]) & !esta[in]) {
					esta[in] = true;
					index[i] = in;
					stay = true;
				} else {
					in++;
				}
			}
		}
		return index;
	}

}
