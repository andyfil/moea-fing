package instanciaInicial;

import java.io.BufferedWriter;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;

public class instanciaInicial {

	public static void main(String[] args) {
		int cantTareas = 1000;
		int cantTareasAltas = 5;
		int cantTareasBajas = 5;
		long cteRandom = 100000*100000;
		long cteAlta = cteRandom*10;
		long cteBaja = cteRandom/10;
		long [] ops_por_tarea = new long[cantTareas];
		double random = 0;
		// Asigno cantidad de operaciones por tareas random
		for (int i=0; i <= cantTareas - cantTareasAltas - cantTareasBajas - 1; i++){
			random = Math.random();
			ops_por_tarea[i] = (long) (random*cteRandom);
		}
		// Asigno cantidad de operaciones por tareas altas
		for (int j=cantTareas - cantTareasAltas - cantTareasBajas; j <= cantTareas - cantTareasBajas - 1; j++){
			random = Math.random();
			ops_por_tarea[j] = (long) (random*cteAlta);
		}
		// Asigno cantidad de operaciones por tareas bajas
		for (int k=cantTareas -  cantTareasBajas; k <= cantTareas - 1; k++){
			random = Math.random();
			ops_por_tarea[k] = (long) (random*cteBaja);
		}
		
		// Creo y armo el archivo con la instancia inicial
		FileOutputStream fos;
		try {
			fos = new FileOutputStream("instancia");
			OutputStreamWriter osw = new OutputStreamWriter(fos)    ;
			BufferedWriter bw      = new BufferedWriter(osw)        ;            
			//bw.write(cantTareas + " ");
			//bw.write(cantMaquinas + " ");
			//bw.write(cantEstados + "\n");
			for (int i=0; i<=cantTareas-1; i++){
				bw.write("t " + i + " " + "ops " + ops_por_tarea[i] + "\n");
			}
			bw.close();
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
/*		// Leo de archivo 4 frentes de pareto independiente del mismo problema y mismo algoritmo
		FileInputStream fis;
		fis = new FileInputStream("C:\\4paretos");
		InputStreamReader isr = new InputStreamReader(fis);
	    //BufferedReader br      = new BufferedReader(isr);  
	    Scanner scan = new Scanner(isr);
	    int i = 0;
	    double makespan;
	    double energy;
	    double [][] paretos = new double[40][2]; 
	    while (scan.hasNext()){
	    	//makespan = scan.nextDouble();
	    	String token = scan.next();
	    	makespan = Double.parseDouble(token);
	    	
	    	token = scan.next();
	    	energy = Double.parseDouble(token);
	    	
	    	paretos[i][0] = makespan;
	    	paretos[i][1] = energy;
	    		    	
	    	i++;
	    }
	    scan.close();
	    
	    System.out.println("FRENTE DE PARETO EMPIRICO RESULTANTE:");
	    System.out.println(" ");
	    // Creo el frente de pareto empirico
	    int k = 0;
	    int indice = -1;
	    boolean parar = false;
	    double [][] frente_pareto = new double[40][2];
	    for (int j=0; j<40; j++){
	    	k=0;
	    	while (k<40 & !parar){
	    		if (j!=k & (paretos[k][0] < paretos[j][0]) & (paretos[k][1] < paretos[j][1])){
	    			parar = true;
	    		}
	    		k++;
	    	}
	    	if (k == 40 & (!parar)){
	    		indice++;
	    		frente_pareto[indice][0] = paretos[j][0];
	    		frente_pareto[indice][1] = paretos[j][1];
	    		System.out.print(frente_pareto[indice][0]);
	    		System.out.print(" ");
	    		System.out.println(frente_pareto[indice][1]);

	    	}
	    }

	    
	    FileOutputStream fos1;
		try {
			fos1 = new FileOutputStream("C:\\Users\\usuario\\workspace\\MetalEJ2\\paretoFronts\\pareto_study");
			OutputStreamWriter osw1 = new OutputStreamWriter(fos1)    ;
			BufferedWriter bw1      = new BufferedWriter(osw1)        ;            
			//bw.write(cantTareas + " ");
			//bw.write(cantMaquinas + " ");
			//bw.write(cantEstados + "\n");
			for (int m=0; m<frente_pareto.length; m++){
				if (frente_pareto[m][0] != 0)
					bw1.write(frente_pareto[m][0] + " " + frente_pareto[m][1] + "\n");
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
	}

}
