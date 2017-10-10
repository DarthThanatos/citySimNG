package py4jmediator.MapResponses;

import java.util.Map;

public class BasicResponse {
    Map<String, Integer> actualResourcesValues;
    Map<String, Integer> actualResourcesIncomes;
    Map<String, Integer> actualResourcesConsumption;
    Map<String, Integer> resourcesBalance;
    int currentDwellersAmount;
    int currentDwellersMaxAmount;

    public BasicResponse(Map<String, Integer> actualResourcesValues, Map<String, Integer> actualResourcesIncomes,
                         Map<String, Integer> actualResourcesConsumption, Map<String, Integer> resourcesBalance,
                         int currentDwellersAmount, int currentDwellersMaxAmount){
        this.actualResourcesValues = actualResourcesValues;
        this.actualResourcesIncomes = actualResourcesIncomes;
        this.actualResourcesConsumption = actualResourcesConsumption;
        this.resourcesBalance = resourcesBalance;
        this.currentDwellersAmount = currentDwellersAmount;
        this.currentDwellersMaxAmount = currentDwellersMaxAmount;
    }

    public Map<String, Integer> getActualResourcesValues() {
        return actualResourcesValues;
    }


    public Map<String, Integer> getActualResourcesIncomes() {
        return actualResourcesIncomes;
    }

    public Map<String, Integer> getActualResourcesConsumption() {
        return actualResourcesConsumption;
    }

    public Map<String, Integer> getResourcesBalance() {
        return resourcesBalance;
    }
    public int getCurrentDwellersAmount() {
        return currentDwellersAmount;
    }

    public int getCurrentDwellersMaxAmount() {
        return currentDwellersMaxAmount;
    }

}
