package py4jmediator;

import constants.Consts;
import entities.Building;
import entities.Dweller;
import entities.Resource;
import py4jmediator.MapResponses.DeleteBuildingResponse;
import py4jmediator.MapResponses.PlaceBuildingResponse;
import py4jmediator.MapResponses.StopProductionResponse;

import java.util.List;
import java.util.Map;
import java.util.logging.Level;
import java.util.logging.Logger;

public class MapPresenter {
    private OnMapPresenterCalled onMapPresenterCalled;
    private static final Logger logger = Logger.getLogger( MapPresenter.class.getName() );


    MapPresenter(){
        logger.setLevel(Consts.DEBUG_LEVEL);
    }

    public interface OnMapPresenterCalled{
        void onGoToMenu();
        void onViewInitialized();
        PlaceBuildingResponse onPlaceBuilding(String buildingName, String buildingId);
        boolean onCheckIfCanAffordOnBuilding(String buildingName);
        DeleteBuildingResponse onDeleteBuilding(String buildingId);
        StopProductionResponse onStopProduction(String buildingId);
        Integer onGetWorkingDwellers(String buildingId);
    }

    public void setOnMapPresenterCalled(OnMapPresenterCalled onMapPresenterCalled){
        this.onMapPresenterCalled = onMapPresenterCalled;
    }

    public void goToMenu(){
        if(onMapPresenterCalled != null){
            logger.log(Level.INFO, "Going to menu");
            onMapPresenterCalled.onGoToMenu();
        }
    }

    public PlaceBuildingResponse placeBuilding(String buildingName, String buildingId){
        if(onMapPresenterCalled != null) {
            logger.log(Level.INFO, "Ordering to place building");
            return onMapPresenterCalled.onPlaceBuilding(buildingName, buildingId);
        }
        return null;
    }

    public boolean checkIfCanAffordOnBuilding(String buildingName){
        if(onMapPresenterCalled != null){
            boolean canAfford =  onMapPresenterCalled.onCheckIfCanAffordOnBuilding(buildingName);
            logger.log(Level.INFO, "Can afford: " + canAfford);
            return canAfford;
        }
        return false;
    }

    public DeleteBuildingResponse deleteBuilding(String buildingId){
        if(onMapPresenterCalled != null) {
            logger.log(Level.INFO, "Ordering to delete building");
            return onMapPresenterCalled.onDeleteBuilding(buildingId);
        }
        return null;
    }

    public StopProductionResponse stopProduction(String buildingId){
        if(onMapPresenterCalled != null) {
            logger.log(Level.INFO, "Ordering to stop production in a building");
            return onMapPresenterCalled.onStopProduction(buildingId);
        }
        return null;
    }

    public Integer getWorkingDwellers(String buildingId){
        if(onMapPresenterCalled != null) {
            logger.log(Level.INFO, "Getting working dwellers in a building");
            return onMapPresenterCalled.onGetWorkingDwellers(buildingId);
        }
        return -1;
    }

    public void viewInitialized(){
        if(onMapPresenterCalled != null) {
            logger.log(Level.INFO, "Acting upon Map View initialization");
            onMapPresenterCalled.onViewInitialized();
        }
    }

    public void displayMap(){
        logger.log(Level.INFO, "Calling Map View Model, displaying map");
        Presenter.getInstance().getViewModel().getMapViewModel().displayMap();
    }

    public void init(List<Resource> resources, List<Building> domesticBuildings,
                     List<Building> industrialBuildings,
                     List<Dweller> dwellers, String texture_one,
                     String texture_two, String panelTexture, String mp3, Map<String, Integer> initialResourcesValues,
                     Map<String, Integer> initialResourcesIncomes,
                     Map<String, Integer> initialResourcesConsumption,
                     Map<String, Integer> initialResourcesBalance,
                     int availableDwellers){
        logger.log(Level.INFO, "Calling Map View Model, init map");
        Presenter.getInstance().getViewModel().getMapViewModel().init(
                resources,
                domesticBuildings,
                industrialBuildings,
                dwellers,
                texture_one,
                texture_two,
                panelTexture,
                mp3,
                initialResourcesValues,
                initialResourcesIncomes,
                initialResourcesConsumption,
                initialResourcesBalance,
                availableDwellers);
    }

    public void updateValuesForCycle(Map<String, Integer> actualResourcesValues,
                                     Map<String, Integer> actualResourcesIncomes,
                                     Map<String, Integer> actualResourcesConsumption,
                                     Map<String, Integer> resourcesBalance,
                                     Integer neededDwellers,
                                     Integer availableDwellers){
        Presenter.getInstance().getViewModel().getMapViewModel().updateValuesForCycle(
                actualResourcesValues,
                actualResourcesIncomes,
                actualResourcesConsumption,
                resourcesBalance,
                neededDwellers,
                availableDwellers);
    }

    public void resumeGame(){
        logger.log(Level.INFO, "Calling Map View Model, resuming game");
        Presenter.getInstance().getViewModel().getMapViewModel().resumeGame();
    }
}
