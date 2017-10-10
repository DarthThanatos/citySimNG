package py4jmediator.MapResponses;

import java.util.List;
import java.util.Map;

public class PlaceBuildingResponse extends BasicResponse {
    public List<String> getEnabledBuildings() {
        return enabledBuildings;
    }

    private List<String> enabledBuildings;

    public PlaceBuildingResponse(Map<String, Integer> actualResourcesValues, Map<String, Integer> actualResourcesIncomes,
                                 Map<String, Integer> actualResourcesConsumption, Map<String, Integer> resourcesBalance,
                                 int currentDwellersAmount, int currentDwellersMaxAmount, List<String> enabledBuildings){
        super(actualResourcesValues, actualResourcesIncomes, actualResourcesConsumption, resourcesBalance,
                currentDwellersAmount, currentDwellersMaxAmount);
        this.enabledBuildings = enabledBuildings;
    }
}
