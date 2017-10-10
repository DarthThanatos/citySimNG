package py4jmediator;

import entities.Building;
import entities.Resource;
import javafx.scene.paint.Stop;
import py4jmediator.MapResponses.DeleteBuildingResponse;
import py4jmediator.MapResponses.PlaceBuildingResponse;
import py4jmediator.MapResponses.StopProductionResponse;

import java.util.List;
import java.util.Map;

public class MapPresenter {
    private OnMapPresenterCalled onMapPresenterCalled;

    public interface OnMapPresenterCalled{
        void onGoToMenu();
        void onViewInitialized();
        PlaceBuildingResponse onPlaceBuilding(String buildingName, String buildingId);
        boolean onCheckIfCanAffordOnBuilding(String buildingName);
        DeleteBuildingResponse onDeleteBuilding(String buildingId);
        StopProductionResponse onStopProduction(String buildingId);
    }

    public void setOnMapPresenterCalled(OnMapPresenterCalled onMapPresenterCalled){
        this.onMapPresenterCalled = onMapPresenterCalled;
    }

    public void goToMenu(){
    	System.out.println("Going to menu");
        if(onMapPresenterCalled != null){
        	System.out.println("map presenter not null");
            onMapPresenterCalled.onGoToMenu();
        }
    }

    public PlaceBuildingResponse placeBuilding(String buildingName, String buildingId){
        if(onMapPresenterCalled != null)
            return onMapPresenterCalled.onPlaceBuilding(buildingName, buildingId);
        return null;
    }

    public boolean checkIfCanAffordOnBuilding(String buildingName){
    	System.out.println("Checking if can afford");
        if(onMapPresenterCalled != null){
        	System.out.println("mapPresenter not null");
            boolean canAfford =  onMapPresenterCalled.onCheckIfCanAffordOnBuilding(buildingName);
        	System.out.println("Can afford: " + canAfford);
            return canAfford;
        }
        return false;
    }

    public DeleteBuildingResponse deleteBuilding(String buildingId){
        if(onMapPresenterCalled != null)
            return onMapPresenterCalled.onDeleteBuilding(buildingId);
        return null;
    }

    public StopProductionResponse stopProduction(String buildingId){
        if(onMapPresenterCalled != null)
            return onMapPresenterCalled.onStopProduction(buildingId);
        return null;
    }

    public void viewInitialized(){
        if(onMapPresenterCalled != null)
            onMapPresenterCalled.onViewInitialized();
    }

    public void displayMap(){
        Presenter.getInstance().getViewModel().getMapViewModel().displayMap();
    }

    public void init(List<Resource> resources, List<Building> buildings, String texture_one, String texture_two,
                     Map<String, Integer> initialResourcesValues, Map<String, Integer> initialResourcesIncomes,
                     Map<String, Integer> initialResourcesConsumption, Map<String, Integer> initialResourcesBalance){
        Presenter.getInstance().getViewModel().getMapViewModel().init(
                resources,
                buildings,
                texture_one,
                texture_two,
                initialResourcesValues,
                initialResourcesIncomes,
                initialResourcesConsumption,
                initialResourcesBalance);
    }

    public void updateResourcesValues(Map<String, Integer> actualResourcesValues,
                                      Map<String, Integer> actualResourcesIncomes,
                                      Map<String, Integer> actualResourcesConsumption,
                                      Map<String, Integer> resourcesBalance){
        Presenter.getInstance().getViewModel().getMapViewModel().updateResourcesValues(
                actualResourcesValues,
                actualResourcesIncomes,
                actualResourcesConsumption,
                resourcesBalance);
    }

    public void resumeGame(){
        Presenter.getInstance().getViewModel().getMapViewModel().resumeGame();
    }
}
