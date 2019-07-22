import InicializarPoblacion.InicializarPoblacion;
import estructurasDatos.DominioDelProblema.Entrada;
import estructurasDatos.Parametros;
import estructurasDatos.ParametrosAlgoritmo;
import estructurasDatos.Solucion;
import main.Main_VNS;
import patrones.Patrones;
import pruebasCasos.DeciderCase;

import java.util.ArrayList;
import java.util.List;

import static main.Main.*;

public class AjusteParametricoVNS {


    public static void main(String[] args) {
        int nEjecucion = 1;
        int[] casos = {1/*, 3, 4, 5, 6, 7, 8, 9*/};
        for (int i = 0; i < casos.length; i++)
            main1(nEjecucion, "Caso" + casos[i]);
    }

    public static void main1(int ejecucion, String caso) {
        /*INICIALIZACION DE DATOS*/
        DeciderCase.switchCase(caso);

        // Carga de los parámetros del dominio del problema:
        Parametros parametros = new Parametros(propFileParameters, propFileOptions);

        // Carga de los parámetros del algoritmo
        ParametrosAlgoritmo parametrosAlgoritmo = new ParametrosAlgoritmo();

        Entrada entrada = Entrada.leerEntrada(parametros, entradaPath, entradaId, entorno);
        Patrones patrones = new Patrones(entrada, parametros);

        carpetaSoluciones = "resultados/" + entradaPath + entradaId + "/" + parametrosAlgoritmo.getAlgoritmo() + "/Soluciones/";
        carpetaTrazas = "resultados/" + entradaPath + entradaId + "/" + parametrosAlgoritmo.getAlgoritmo() + "/Trazas/";

        // OUTPUT ///////////////////////////////////////////////////////////////////////////////////////////////////
        ArrayList<Solucion> solEntrada = new ArrayList<>();
        solEntrada.add(entrada.getDistribucionInicial());
        /////////////////////////////////////////////////////////////////////////////////////////////////////////////


        // la distribucion inicial está en "entrada"
        ArrayList<Solucion> poblacionInicial = InicializarPoblacion.inicializarPoblacion(entrada, parametros, patrones);

        // OUTPUT ///////////////////////////////////////////////////////////////////////////////////////////////////
        solEntrada.addAll(poblacionInicial);
        /////////////////////////////////////////////////////////////////////////////////////////////////////////////

        switch (parametrosAlgoritmo.getAlgoritmo()) {
            case "VNS":
                execute10TimesVNSAndSave(caso, parametros, parametrosAlgoritmo, entrada, patrones, poblacionInicial, solEntrada);

                System.err.println("x---------------x");
                parametrosAlgoritmo.setMaxMilisecondsAllowed(10 * 60000);
                execute10TimesVNS(caso, parametros, parametrosAlgoritmo, entrada, patrones, poblacionInicial, solEntrada);

                System.err.println("x---------------x");
                parametrosAlgoritmo.setMaxMilisecondsAllowed(15 * 60000);
                execute10TimesVNSAndSave(caso, parametros, parametrosAlgoritmo, entrada, patrones, poblacionInicial, solEntrada);

                System.err.println("x---------------x");
                parametrosAlgoritmo.setMaxMilisecondsAllowed(20 * 60000);
                execute10TimesVNS(caso, parametros, parametrosAlgoritmo, entrada, patrones, poblacionInicial, solEntrada);

                System.err.println("x---------------x");
                parametrosAlgoritmo.setMaxMilisecondsAllowed(25 * 60000);
                execute10TimesVNSAndSave(caso, parametros, parametrosAlgoritmo, entrada, patrones, poblacionInicial, solEntrada);

                System.err.println("x---------------x");
                parametrosAlgoritmo.setMaxMilisecondsAllowed(30 * 60000);
                execute10TimesVNS(caso, parametros, parametrosAlgoritmo, entrada, patrones, poblacionInicial, solEntrada);

                System.err.println("x---------------x");
                parametrosAlgoritmo.setMaxMilisecondsAllowed(35 * 60000);
                execute10TimesVNSAndSave(caso, parametros, parametrosAlgoritmo, entrada, patrones, poblacionInicial, solEntrada);

                System.err.println("x---------------x");
                parametrosAlgoritmo.setMaxMilisecondsAllowed(40 * 60000);
                execute10TimesVNS(caso, parametros, parametrosAlgoritmo, entrada, patrones, poblacionInicial, solEntrada);

                System.err.println("x---------------x");
                parametrosAlgoritmo.setMaxMilisecondsAllowed(45 * 60000);
                execute10TimesVNSAndSave(caso, parametros, parametrosAlgoritmo, entrada, patrones, poblacionInicial, solEntrada);

                System.err.println("x---------------x");
                parametrosAlgoritmo.setMaxMilisecondsAllowed(50 * 60000);
                execute10TimesVNS(caso, parametros, parametrosAlgoritmo, entrada, patrones, poblacionInicial, solEntrada);

                System.err.println("x---------------x");
                parametrosAlgoritmo.setMaxMilisecondsAllowed(55 * 60000);
                execute10TimesVNS(caso, parametros, parametrosAlgoritmo, entrada, patrones, poblacionInicial, solEntrada);

                System.err.println("x---------------x");
                parametrosAlgoritmo.setMaxMilisecondsAllowed(60 * 60000);
                execute10TimesVNSAndSave(caso, parametros, parametrosAlgoritmo, entrada, patrones, poblacionInicial, solEntrada);


                break;

            default:
                System.err.println("Algoritmo \"" + parametrosAlgoritmo.getAlgoritmo() + "\" no encontrado.");
                break;
        }

        // OUTPUT ///////////////////////////////////////////////////////////////////////////////////////////////////
        String sb = caso + "-" + ejecucion;
        rwFiles.EscrituraExcel.EscrituraSoluciones(sb/*caso + "-" /*+ ejecucion*/ /*+ "-Inicial+Fase1+Fase2"*/,
                main.Main.carpetaSoluciones, solEntrada, entrada, patrones, parametros, parametrosAlgoritmo);
        /////////////////////////////////////////////////////////////////////////////////////////////////////////////

    }

    private static void execute10TimesVNS(String caso, Parametros parametros, ParametrosAlgoritmo parametrosAlgoritmo,
                                          Entrada entrada, Patrones patrones, List<Solucion> poblacionInicial,
                                          List<Solucion> solEntrada) {
        for (int i = 0; i < 10; i++)
            Main_VNS.main_vns(caso, parametros, parametrosAlgoritmo, entrada, patrones, poblacionInicial);
    }

    private static void execute10TimesVNSAndSave(String caso, Parametros parametros, ParametrosAlgoritmo parametrosAlgoritmo,
                                          Entrada entrada, Patrones patrones, List<Solucion> poblacionInicial,
                                          List<Solucion> solEntrada) {
        for (int i = 0; i < 10; i++) {
            List<Solucion> r =
                    Main_VNS.main_vns(caso, parametros, parametrosAlgoritmo, entrada, patrones, poblacionInicial);
            if (i == 9) solEntrada.addAll(r);
        }

    }

}
