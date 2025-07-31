// ReceptorCRC32.java
import java.io.*;
import java.net.*;
import java.util.zip.CRC32;

public class ReceptorCRC32 {

    // CAPA 5: TRANSMISIÓN
    public static String recibirTrama(String host, int puerto) throws IOException {
        System.out.println("--- CAPA DE TRANSMISIÓN ---");
        ServerSocket server = new ServerSocket();
        server.setReuseAddress(true);
        server.bind(new InetSocketAddress(host, puerto));
        System.out.printf("Escuchando en %s:%d...%n", host, puerto);

        Socket client = server.accept();
        System.out.printf("Conexión establecida desde %s%n", client.getRemoteSocketAddress());

        BufferedReader in = new BufferedReader(new InputStreamReader(client.getInputStream()));
        StringBuilder sb = new StringBuilder();
        String line;
        // asume que toda la trama viene en una sola línea
        while ((line = in.readLine()) != null) {
            sb.append(line);
        }
        client.close();
        server.close();

        System.out.println("Trama recibida.");
        return sb.toString();
    }

    // CAPA 3: ENLACE
    public static Result verificarIntegridad(String trama) {
        System.out.println("\n--- CAPA DE ENLACE ---");
        if (trama == null || trama.length() < 32) {
            System.err.println("Error: trama inválida o demasiado corta.");
            return new Result(null, null, true);
        }

        String mensajeBin = trama.substring(0, trama.length() - 32);
        String crcRecibido = trama.substring(trama.length() - 32);
        System.out.println("CRC recibido:  " + crcRecibido);

        // reconvertir binario a texto
        StringBuilder texto = new StringBuilder();
        for (int i = 0; i < mensajeBin.length(); i += 8) {
            String byteStr = mensajeBin.substring(i, i + 8);
            texto.append((char) Integer.parseInt(byteStr, 2));
        }

        // calcular CRC32
        CRC32 crc32 = new CRC32();
        crc32.update(texto.toString().getBytes());
        String crcCalc = String.format("%32s", Long.toBinaryString(crc32.getValue() & 0xFFFFFFFFL))
                             .replace(' ', '0');
        System.out.println("CRC calculado: " + crcCalc);

        boolean error = !crcCalc.equals(crcRecibido);
        System.out.println(error
            ? "Error detectado en la transmisión (CRC diferente)."
            : "No se detectaron errores (CRC coincide).");

        return new Result(mensajeBin, texto.toString(), error);
    }

    // CAPA 2+1: PRESENTACIÓN y APLICACIÓN
    public static void procesarMensaje(Result r) {
        System.out.println("\n--- CAPA DE PRESENTACIÓN ---");
        if (r.error) {
            System.out.println("No es posible decodificar el mensaje debido a errores detectados.");
            return;
        }
        System.out.println("--- CAPA DE APLICACIÓN ---");
        System.out.println("Mensaje recibido correctamente:");
        System.out.println(r.texto);
    }

    public static void main(String[] args) throws IOException {
        System.out.println("--- RECEPTOR INICIADO ---");
        String trama = recibirTrama("localhost", 5000);
        Result r = verificarIntegridad(trama);
        procesarMensaje(r);
    }

    // Helper para retornar múltiples valores
    private static class Result {
        String binario, texto;
        boolean error;
        Result(String b, String t, boolean e) {
            binario = b; texto = t; error = e;
        }
    }
}
