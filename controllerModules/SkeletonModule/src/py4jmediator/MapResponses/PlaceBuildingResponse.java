package py4jmediator.MapResponses;

import entities.Building;

import java.util.List;
import java.util.Map;

public class PlaceBuildingResponse extends BasicResponse {
    private List<String> enabledBuildings;
    private Integer workingDwellers;

    public PlaceBuildingResponse(Map<String, Integer> actualResourcesValues, Map<String, Integer> actualResourcesIncomes,
                                 Map<String, Integer> actualResourcesConsumption, Map<String, Integer> resourcesBalance,
                                 int currentDwellersAmount, int currentDwellersMaxAmount, List<String> enabledBuildings,
                                 Integer workingDwellers){
        super(actualResourcesValues, actualResourcesIncomes, actualResourcesConsumption, resourcesBalance,
                currentDwellersAmount, currentDwellersMaxAmount);
        this.enabledBuildings = enabledBuildings;
        this.workingDwellers = workingDwellers;
    }

    /* Getters and setters */
    public List<String> getEnabledBuildings() {
        return enabledBuildings;
    }

    public Integer getWorkingDwellers() {
        return workingDwellers;
    }

}
