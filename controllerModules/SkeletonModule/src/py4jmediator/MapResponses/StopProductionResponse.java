package py4jmediator.MapResponses;

import java.util.List;
import java.util.Map;

public class StopProductionResponse extends BasicResponse {
    public boolean isRunning() {
        return isRunning;
    }

    private boolean isRunning;

    public StopProductionResponse(Map<String, Integer> actualResourcesValues, Map<String, Integer> actualResourcesIncomes,
                                 Map<String, Integer> actualResourcesConsumption, Map<String, Integer> resourcesBalance,
                                 int currentDwellersAmount, int currentDwellersMaxAmount, boolean isRunning){
        super(actualResourcesValues, actualResourcesIncomes, actualResourcesConsumption, resourcesBalance,
                currentDwellersAmount, currentDwellersMaxAmount);
        this.isRunning = isRunning;
    }
}
