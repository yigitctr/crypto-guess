import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;

import javax.swing.JFrame;

import org.apache.commons.math3.stat.regression.SimpleRegression;
import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartPanel;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.plot.PlotOrientation;
import org.jfree.data.xy.XYSeries;
import org.jfree.data.xy.XYSeriesCollection;

import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonParser;

public class CryptoPrediction {
    public static void main(String[] args) {
        try {
           
            String url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=365";
            String jsonResponse = getJSON(url);
            List<Double> prices = parsePrices(jsonResponse);

           
            plotData(prices);

            
            SimpleRegression regression = new SimpleRegression();
            for (int i = 0; i < prices.size(); i++) {
                regression.addData(i, prices.get(i));
            }

          
            int forecastDays = 30;
            List<Double> forecastPrices = new ArrayList<>();
            for (int i = prices.size(); i < prices.size() + forecastDays; i++) {
                forecastPrices.add(regression.predict(i));
            }

            
            plotForecast(prices, forecastPrices);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private static String getJSON(String url) throws Exception {
        HttpURLConnection conn = (HttpURLConnection) new URL(url).openConnection();
        conn.setRequestMethod("GET");
        BufferedReader in = new BufferedReader(new InputStreamReader(conn.getInputStream()));
        String inputLine;
        StringBuilder response = new StringBuilder();
        while ((inputLine = in.readLine()) != null) {
            response.append(inputLine);
        }
        in.close();
        return response.toString();
    }

    private static List<Double> parsePrices(String jsonResponse) {
        List<Double> prices = new ArrayList<>();
        JsonElement jsonElement = JsonParser.parseString(jsonResponse);
        JsonArray pricesArray = jsonElement.getAsJsonObject().get("prices").getAsJsonArray();
        for (JsonElement priceElement : pricesArray) {
            prices.add(priceElement.getAsJsonArray().get(1).getAsDouble());
        }
        return prices;
    }

    private static void plotData(List<Double> prices) {
        XYSeries series = new XYSeries("Bitcoin Prices");
        for (int i = 0; i < prices.size(); i++) {
            series.add(i, prices.get(i));
        }
        XYSeriesCollection dataset = new XYSeriesCollection(series);
        JFreeChart chart = ChartFactory.createXYLineChart(
                "Bitcoin Prices Over Time",
                "Days",
                "Price",
                dataset,
                PlotOrientation.VERTICAL,
                true,
                true,
                false
        );
        displayChart(chart);
    }

    private static void plotForecast(List<Double> prices, List<Double> forecastPrices) {
        XYSeries observedSeries = new XYSeries("Observed Prices");
        for (int i = 0; i < prices.size(); i++) {
            observedSeries.add(i, prices.get(i));
        }
        XYSeries forecastSeries = new XYSeries("Forecast Prices");
        for (int i = 0; i < forecastPrices.size(); i++) {
            forecastSeries.add(prices.size() + i, forecastPrices.get(i));
        }
        XYSeriesCollection dataset = new XYSeriesCollection();
        dataset.addSeries(observedSeries);
        dataset.addSeries(forecastSeries);
        JFreeChart chart = ChartFactory.createXYLineChart(
                "Bitcoin Price Forecast",
                "Days",
                "Price",
                dataset,
                PlotOrientation.VERTICAL,
                true,
                true,
                false
        );
        displayChart(chart);
    }

    private static void displayChart(JFreeChart chart) {
        JFrame frame = new JFrame();
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.add(new ChartPanel(chart));
        frame.pack();
        frame.setVisible(true);
    }
}
