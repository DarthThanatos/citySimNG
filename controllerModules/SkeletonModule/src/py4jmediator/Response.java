package py4jmediator;

import java.util.Map;

public class Response {
    Map<String, Integer> actualResourcesValues;
    Map<String, Integer> actualResourcesIncomes;
    int currentDwellersAmount;
    int currentDwellersMaxAmount;
    boolean isBuildingRunning;

    public Response(Map<String, Integer> actualResourcesValues, Map<String, Integer> actualResourcesIncomes,
             int currentDwellersAmount, int currentDwellersMaxAmount){
        this.actualResourcesValues = actualResourcesValues;
        this.actualResourcesIncomes = actualResourcesIncomes;
        this.currentDwellersAmount = currentDwellersAmount;
        this.currentDwellersMaxAmount = currentDwellersMaxAmount;
    }

    public Response(Map<String, Integer> actualResourcesValues, Map<String, Integer> actualResourcesIncomes,
             int currentDwellersAmount, int currentDwellersMaxAmount, boolean isBuildingRunning){
        this.actualResourcesValues = actualResourcesValues;
        this.actualResourcesIncomes = actualResourcesIncomes;
        this.currentDwellersAmount = currentDwellersAmount;
        this.currentDwellersMaxAmount = currentDwellersMaxAmount;
        this.isBuildingRunning = isBuildingRunning;
    }

    public Map<String, Integer> getActualResourcesValues() {
        return actualResourcesValues;
    }

    public Map<String, Integer> getActualResourcesIncomes() {
        return actualResourcesIncomes;
    }

    public int getCurrentDwellersAmount() {
        return currentDwellersAmount;
    }

    public int getCurrentDwellersMaxAmount() {
        return currentDwellersMaxAmount;
    }

    public boolean isBuildingRunning() {
        return isBuildingRunning;
    }
}
