import com.google.common.collect.ImmutableMap;
import entities.Building;
import entities.Dweller;
import entities.Resource;
import junitparams.JUnitParamsRunner;
import junitparams.Parameters;
import mapnode.Buildings;
import mapnode.Dwellers;
import mapnode.Resources;
import model.DependenciesRepresenter;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import java.util.*;
import static junitparams.JUnitParamsRunner.$;
import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

@RunWith(JUnitParamsRunner.class)
public class MixedUnitTest {
    private static final String DOMESTIC = "domestic";
    private static final String INDUSTRIAL = "industrial";

    @Mock
    private static DependenciesRepresenter dependenciesRepresenter;

    private static Map<String, Building> buildingsMap;
    private static Map<String, Integer> resourcesMap = new LinkedHashMap<>();

    @BeforeClass
    public static void initializeClass(){
        resourcesMap.put("Wood", 0);
        resourcesMap.put("Gold", 0);
        resourcesMap.put("Grain", 0);
        resourcesMap.put("Flour", 0);
        resourcesMap.put("Bread", 0);
    }

    @Before
    public void initializeTest(){
        dependenciesRepresenter = mock(DependenciesRepresenter.class);

        // add dwellers
        List<Dweller> allDwellers = new ArrayList<>();

        Dweller worker = new Dweller("Worker", "None", "None", "", "");

        allDwellers.add(worker);

        when(dependenciesRepresenter.getModuleData("allDwellers")).thenReturn(allDwellers);

        // add buildings
        buildingsMap = new HashMap<>();

        Map<String, Integer> fieldProduces = new HashMap<>(resourcesMap);
        fieldProduces.put("Grain", 3);
        Map<String, Integer> fieldConsumes = new HashMap<>(resourcesMap);
        fieldConsumes.put("Gold", 3);
        Map<String, Integer> fieldResourcesCost = new HashMap<>(resourcesMap);
        fieldResourcesCost.put("Wood", 10);
        Building field = new Building("Field", "None", "None", 2, fieldProduces,
                fieldConsumes, fieldResourcesCost, "", "Industrial", "", "Worker");
        buildingsMap.put(field.getName(), field);

        Map<String, Integer> millProduces = new HashMap<>(resourcesMap);
        millProduces.put("Flour", 3);
        Map<String, Integer> millConsumes = new HashMap<>(resourcesMap);
        millConsumes.put("Grain", 2);
        Map<String, Integer> millResourcesCost = new HashMap<>(resourcesMap);
        millResourcesCost.put("Wood", 13);
        Building mill = new Building("Mill", "Field", "None", 3, millProduces,
                millConsumes, millResourcesCost, "", "Industrial", "", "Worker");
        buildingsMap.put(mill.getName(), mill);

        Map<String, Integer> houseProduces = new HashMap<>(resourcesMap);
        houseProduces.put("Gold", 1);
        Map<String, Integer> houseConsumes = new HashMap<>(resourcesMap);
        houseConsumes.put("Bread", 1);
        Map<String, Integer> houseResourcesCost = new HashMap<>(resourcesMap);
        houseResourcesCost.put("Wood", 15);

        Building house = new Building("House", "None", "None", 2, houseProduces,
                houseConsumes, houseResourcesCost, "", "Domestic", "", "Worker");
        buildingsMap.put(house.getName(), house);

        when(dependenciesRepresenter.getModuleData("allBuildings")).thenReturn(new ArrayList<>(buildingsMap.values()));

        // add resources
        List<Resource> resourcesList = new ArrayList<>();

        Resource r1 = new Resource("Wood", "None", "None", "", "", 3);
        Resource r2 = new Resource("Grain", "None", "None", "", "", 0);
        Resource r3 = new Resource("Gold", "None", "None", "", "", 0);
        Resource r4 = new Resource("Bread", "None", "None", "", "", 0);
        Resource r5 = new Resource("Flour", "None", "None", "", "", 0);

        resourcesList.add(r1);
        resourcesList.add(r2);
        resourcesList.add(r3);
        resourcesList.add(r4);
        resourcesList.add(r5);

        Map<String, Integer> basicResourcesIncome = new HashMap<>(resourcesMap);
        basicResourcesIncome.put("Wood", 3);

        when(dependenciesRepresenter.getModuleData("resourcesList")).thenReturn(resourcesList);
        when(dependenciesRepresenter.getModuleData("incomes")).thenReturn(basicResourcesIncome);
    }

    private Object[] parametersForPlaceBuildingTest() {
        return $(
                $(ImmutableMap.of("Wood", 15, "Gold", 5), 2, "Field", "FieldId12345", "Field",
                        "FieldId123456", 0, 2, ImmutableMap.of("Wood", 5, "Gold", 2),
                        ImmutableMap.of("Gold", 3), ImmutableMap.of("Grain", 3),
                        ImmutableMap.of("Grain", 3, "Gold", -3), true, "Mill", false, false, false),
                $(ImmutableMap.of("Wood", 15, "Bread", 3, "Gold", 5), 0, "House",
                        "HouseID12345", "Field", "FieldId123456", 0, 2,
                        ImmutableMap.of("Wood", 0, "Gold", 2, "Bread", 2),
                        ImmutableMap.of("Bread", 1, "Gold", 3),  ImmutableMap.of("Gold", 1, "Grain", 3),
                        ImmutableMap.of("Gold", -2, "Bread", -1, "Grain", 3),
                        true, "", false, false, true),
                $(ImmutableMap.of("Wood", 15, "Gold", 5), 0, "Field", "FieldId12345",
                        "Field", "FieldId123456", 0, 0, ImmutableMap.of("Wood", 5, "Gold", 5),
                        ImmutableMap.of("Gold", 0), ImmutableMap.of("Grain", 0),
                        ImmutableMap.of("Grain", 0, "Gold", 0), false, "Mill", false, true, false),
                $(ImmutableMap.of("Wood", 15, "Bread", 0), 0, "House", "HouseID12345",
                        "Field", "FieldId123456", 0, 0, ImmutableMap.of("Wood", 0, "Bread", 0),
                        ImmutableMap.of("Bread", 1),  ImmutableMap.of("Gold", 0),
                        ImmutableMap.of("Gold", 0, "Bread", -1), false, "", true, false, false),
                $(ImmutableMap.of("Wood", 15, "Gold", 0), 2, "Field", "FieldId12345",
                        "Field", "FieldId123456", 0, 2, ImmutableMap.of("Wood", 5, "Gold", 0),
                        ImmutableMap.of("Gold", 3),  ImmutableMap.of("Grain", 0),
                        ImmutableMap.of("Grain", 0, "Gold", -3), false, "Mill", true, false, false)
        );
    }

    @Test
    @Parameters(method="parametersForPlaceBuildingTest")
    public void placeBuildingTest(Map<String, Integer> initialResValues, int initialAvailableDwellers,
                                  String newBuildingName, String newBuildingId,
                                  String notFullyOccupiedBuildingName, String notFullyOccupiedBuildingId,
                                  Integer notFullyOccupiedBuildingWorkingDwellers,
                                  Integer expectedNumOfDwellersWorkingInBuilding, Map<String, Integer> expectedResValues,
                                  Map<String, Integer> expectedResConsumption, Map<String, Integer> expectedResIncomes,
                                  Map<String, Integer> expectedResBalance, boolean isNewBuildingProducing,
                                  String unlockedBuilding, boolean isNewBuildingUnprovided,
                                  boolean isNewBuildingNotFullyOccupied, boolean updateNotFullyOccupiedBuildings){
        // given
        Buildings buildings = new Buildings(dependenciesRepresenter);
        Resources resources = new Resources(dependenciesRepresenter);
        Dwellers  dwellers = new Dwellers(dependenciesRepresenter);

        String buildingType = buildingsMap.get(newBuildingName).getType().toLowerCase();

        Building notFullyOccupiedBuilding = createBuilding(buildings, notFullyOccupiedBuildingName,
                notFullyOccupiedBuildingId, notFullyOccupiedBuildingWorkingDwellers);
        buildings.getNotFullyOccupiedBuildings().put(notFullyOccupiedBuildingId, notFullyOccupiedBuilding);

        dwellers.setAvailableDwellers(initialAvailableDwellers);

        for(String resName: initialResValues.keySet())
            resources.getActualResourcesValues().put(resName, initialResValues.get(resName));

        // when
        buildings.placeBuilding(newBuildingName, newBuildingId, resources, dwellers);

        // then
        for(String resName: expectedResValues.keySet())
            assertEquals(resources.getActualResourcesValues().get(resName), expectedResValues.get(resName));

        for(String resName: expectedResConsumption.keySet())
            assertEquals(resources.getActualResourcesConsumption().get(resName), expectedResConsumption.get(resName));

        for(String resName: expectedResBalance.keySet())
            assertEquals(resources.getResourcesBalance().get(resName), expectedResBalance.get(resName));

        for(String resName: expectedResIncomes.keySet())
            assertEquals(resources.getActualResourcesIncomes().get(resName), expectedResIncomes.get(resName));

        if(isNewBuildingUnprovided)
            assertTrue(buildings.getUnprovidedBuildings().containsKey(newBuildingId));

        Building newBuilding;
        if(buildingType.equals(DOMESTIC))
            newBuilding = buildings.getPlayerDomesticBuildings().get(newBuildingId);
        else
            newBuilding = buildings.getPlayerIndustrialBuildings().get(newBuildingId);

        assertNotNull(newBuilding);
        assertEquals(newBuildingId, newBuilding.getId());
        assertEquals(newBuilding.isProducing(), isNewBuildingProducing);
        assertEquals(newBuilding.getWorkingDwellers(), expectedNumOfDwellersWorkingInBuilding);

        if(buildingType.equals(DOMESTIC)){
            assertEquals(dwellers.getAvailableDwellers(), initialAvailableDwellers + newBuilding.getWorkingDwellers());
        }
        else{
            assertEquals((Integer) dwellers.getWorkingDwellers(), newBuilding.getWorkingDwellers());
            assertEquals((Integer) dwellers.getNeededDwellers(), newBuilding.getDwellersAmount());
            if(isNewBuildingNotFullyOccupied)
                assertTrue(buildings.getNotFullyOccupiedBuildings().containsKey(newBuildingId));
        }

        if(updateNotFullyOccupiedBuildings) {
            assertFalse(buildings.getNotFullyOccupiedBuildings().containsKey(notFullyOccupiedBuildingId));
            assertTrue(buildings.getNotFullyOccupiedBuildings().isEmpty());
        }
        else
            assertTrue(buildings.getNotFullyOccupiedBuildings().containsKey(notFullyOccupiedBuildingId));

        if(!unlockedBuilding.isEmpty())
            assertTrue(buildingsMap.get(unlockedBuilding).isEnabled());
    }

    private Object[] parametersForDeleteBuildingTest() {
        return $(
                $(ImmutableMap.of("Wood", 7, "Gold", 5), 2, 4, 2, "Field", "FieldId12345", 2,
                        true, true, "Field", "FieldId123456", 0, false, 2,
                        ImmutableMap.of("Wood", 12, "Gold", 2), ImmutableMap.of("Gold", 0),
                        ImmutableMap.of("Grain", 0), ImmutableMap.of("Grain", 0, "Gold", 0)),
                $(ImmutableMap.of("Wood", 7, "Gold", 5), 2, 2, 4, "Field", "FieldId12345", 0,
                        false, false, "Field", "FieldId123456", 2, true, 2,
                        ImmutableMap.of("Wood", 12, "Gold", 5), ImmutableMap.of("Gold", 0),
                        ImmutableMap.of("Grain", 0), ImmutableMap.of("Grain", 0, "Gold", 0)),
                $(ImmutableMap.of("Wood", 7, "Gold", 5), 4, 4, 4, "Field", "FieldId12345", 2,
                        true, false, "Field", "FieldId123456", 2, true, 2,
                        ImmutableMap.of("Wood", 12, "Gold", 5), ImmutableMap.of("Gold", -3),
                        ImmutableMap.of("Grain", 0), ImmutableMap.of("Grain", 0, "Gold", 3)),
                $(ImmutableMap.of("Wood", 7, "Gold", 5), 2, 2, 2, "Field", "FieldId12345", 2,
                        true, true, "House", "HouseId123456", 2, true, 0,
                        ImmutableMap.of("Wood", 12, "Gold", 5), ImmutableMap.of("Gold", -3),
                        ImmutableMap.of("Grain", -3), ImmutableMap.of("Grain", -3, "Gold", 3)),
                $(ImmutableMap.of("Wood", 7, "Bread", 3, "Gold", 5), 2, 2, 2, "House",
                        "HouseId12345", 2, true, true, "Field", "FieldId123456", 2, true, 0,
                        ImmutableMap.of("Wood", 14, "Bread", 3, "Gold", 5),
                        ImmutableMap.of("Bread", -1, "Gold", -3),
                        ImmutableMap.of("Gold", -1, "Grain", -3),
                        ImmutableMap.of("Gold", 2, "Bread", 1, "Grain", -3)),
                $(ImmutableMap.of("Wood", 7, "Bread", 3, "Gold", 5), 2, 2, 4, "House",
                        "HouseId12345", 2, true, true, "Field", "FieldId123456", 2, true, 2,
                        ImmutableMap.of("Wood", 14, "Bread", 3, "Gold", 5),
                        ImmutableMap.of("Bread", -1, "Gold", 0),
                        ImmutableMap.of("Gold", -1, "Grain", 0),
                        ImmutableMap.of("Gold", -1, "Bread", 1, "Grain", 0))
        );
    }

    @Test
    @Parameters(method="parametersForDeleteBuildingTest")
    public void deleteBuildingTest(Map<String, Integer> initialResValues, int initialWorkingDwellers,
                                   int initialNeededDwellers, int initialAvailableDwellers,
                                   String buildingToRemoveName, String buildingToRemoveId,
                                   int buildingToRemoveWorkingDwellers, boolean isBuildingToRemoveRunning,
                                   boolean isBuildingToRemoveProducing, String otherBuildingName, String otherBuildingId,
                                   int otherBuildingWorkingDwellers, boolean isOtherBuildingProducing,
                                   Integer expectedWorkingDwellers, Map<String, Integer> expectedResValues,
                                   Map<String, Integer> expectedResConsumption, Map<String, Integer> expectedResIncomes,
                                   Map<String, Integer> expectedResBalance){
        // given
        Buildings buildings = new Buildings(dependenciesRepresenter);
        Resources resources = new Resources(dependenciesRepresenter);
        Dwellers  dwellers = new Dwellers(dependenciesRepresenter);

        Building buildingToRemove = createBuilding(buildings, buildingToRemoveName, buildingToRemoveId, buildingToRemoveWorkingDwellers);
        buildingToRemove.setProducing(isBuildingToRemoveProducing);
        buildingToRemove.setRunning(isBuildingToRemoveRunning);

        Building otherBuilding = createBuilding(buildings, otherBuildingName, otherBuildingId, otherBuildingWorkingDwellers);
        otherBuilding.setProducing(isOtherBuildingProducing);

        dwellers.setAvailableDwellers(initialAvailableDwellers);
        dwellers.setWorkingDwellers(initialWorkingDwellers);
        dwellers.setNeededDwellers(initialNeededDwellers);

        if(buildingToRemove.getType().toLowerCase().equals(INDUSTRIAL)
                && otherBuilding.getType().toLowerCase().equals(INDUSTRIAL))
            buildings.getNotFullyOccupiedBuildings().put(otherBuildingId, otherBuilding);

        for(String resName: initialResValues.keySet())
            resources.getActualResourcesValues().put(resName, initialResValues.get(resName));

        // when
        buildings.deleteBuilding(buildingToRemoveId, resources, dwellers);

        // then
        for(String resName: expectedResValues.keySet())
            assertEquals(resources.getActualResourcesValues().get(resName), expectedResValues.get(resName));

        if(isBuildingToRemoveRunning){
            if(isBuildingToRemoveProducing && buildingToRemove.getType().toLowerCase().equals(DOMESTIC)){
                assertEquals(dwellers.getAvailableDwellers(), initialAvailableDwellers - buildingToRemove.getWorkingDwellers());
                assertEquals(otherBuilding.getWorkingDwellers(), expectedWorkingDwellers);
            }

            if(buildingToRemove.getType().toLowerCase().equals(INDUSTRIAL)){
                assertEquals(dwellers.getNeededDwellers(), initialNeededDwellers - buildingToRemove.getDwellersAmount());
                assertEquals((Integer)dwellers.getWorkingDwellers(), expectedWorkingDwellers);
                assertTrue(buildings.getNotFullyOccupiedBuildings().isEmpty());
                assertEquals(otherBuilding.getWorkingDwellers(), (Integer)Integer.min(buildingToRemove.getWorkingDwellers(), otherBuilding.getDwellersAmount()));
            }

            for(String resName: expectedResConsumption.keySet())
                assertEquals(resources.getActualResourcesConsumption().get(resName), expectedResConsumption.get(resName));

            for(String resName: expectedResIncomes.keySet())
                assertEquals(resources.getActualResourcesIncomes().get(resName), expectedResIncomes.get(resName));

            for(String resName: expectedResBalance.keySet())
                assertEquals(resources.getResourcesBalance().get(resName), expectedResBalance.get(resName));
        }

        if(buildingToRemove.getType().toLowerCase().equals(DOMESTIC))
            assertFalse(buildings.getPlayerDomesticBuildings().containsKey(buildingToRemoveId));
        else
            assertFalse(buildings.getPlayerIndustrialBuildings().containsKey(buildingToRemoveId));
    }

    private Object[] parametersForStopProductionInBuildingTest() {
        return $(
                $(ImmutableMap.of("Wood", 7, "Gold", 5), 2, 4, 2, "Field", "FieldId12345", 2,
                        true, "Field", "FieldId123456", 0, false, 2, 2,
                        ImmutableMap.of("Wood", 7, "Gold", 2), ImmutableMap.of("Gold", 0),
                        ImmutableMap.of("Grain", 0), ImmutableMap.of("Grain", 0, "Gold", 0)),
                $(ImmutableMap.of("Wood", 7, "Gold", 5), 4, 4, 4, "Field", "FieldId12345", 2,
                        false, "Field", "FieldId123456", 2, true, 2, 2,
                        ImmutableMap.of("Wood", 7, "Gold", 5), ImmutableMap.of("Gold", -3),
                        ImmutableMap.of("Grain", 0), ImmutableMap.of("Grain", 0, "Gold", 3)),
                $(ImmutableMap.of("Wood", 7, "Gold", 5), 2, 2, 2, "Field", "FieldId12345", 2,
                        true, "House", "HouseId123456", 2, true, 0, 2,
                        ImmutableMap.of("Wood", 7, "Gold", 5), ImmutableMap.of("Gold", -3),
                        ImmutableMap.of("Grain", -3), ImmutableMap.of("Grain", -3, "Gold", 3)),
                $(ImmutableMap.of("Wood", 7, "Bread", 3, "Gold", 5), 2, 2, 2, "House",
                        "HouseId12345", 2, true, "Field", "FieldId123456", 2, true, 0, 0,
                        ImmutableMap.of("Wood", 7, "Bread", 3, "Gold", 5),
                        ImmutableMap.of("Bread", -1, "Gold", -3),
                        ImmutableMap.of("Gold", -1, "Grain", -3),
                        ImmutableMap.of("Gold", 2, "Bread", 1, "Grain", -3)),
                $(ImmutableMap.of("Wood", 7, "Bread", 3, "Gold", 5), 2, 2, 4, "House",
                        "HouseId12345", 2, true, "Field", "FieldId123456", 2, true, 2, 2,
                        ImmutableMap.of("Wood", 7, "Bread", 3, "Gold", 5),
                        ImmutableMap.of("Bread", -1, "Gold", 0),
                        ImmutableMap.of("Gold", -1, "Grain", 0),
                        ImmutableMap.of("Gold", -1, "Bread", 1, "Grain", 0))
        );
    }

    @Test
    @Parameters(method="parametersForStopProductionInBuildingTest")
    public void stopProductionInBuildingTest(Map<String, Integer> initialResValues, int initialWorkingDwellers,
                                             int initialNeededDwellers, int initialAvailableDwellers,
                                             String buildingName, String buildingId,
                                             int numOfDwellersWorkingInBuilding,
                                             boolean isBuildingProducing, String otherBuildingName, String otherBuildingId,
                                             int otherBuildingWorkingDwellers, boolean isOtherBuildingProducing,
                                             Integer expectedWorkingDwellers, Integer expectedOtherBuildingWorkingDwellers,
                                             Map<String, Integer> expectedResValues, Map<String, Integer> expectedResConsumption,
                                             Map<String, Integer> expectedResIncomes, Map<String, Integer> expectedResBalance){
        // given
        Buildings buildings = new Buildings(dependenciesRepresenter);
        Resources resources = new Resources(dependenciesRepresenter);
        Dwellers  dwellers = new Dwellers(dependenciesRepresenter);

        Building building = createBuilding(buildings, buildingName, buildingId, numOfDwellersWorkingInBuilding);
        building.setProducing(isBuildingProducing);

        Building otherBuilding = createBuilding(buildings, otherBuildingName, otherBuildingId, otherBuildingWorkingDwellers);
        otherBuilding.setProducing(isOtherBuildingProducing);

        if(building.getType().toLowerCase().equals(INDUSTRIAL)
                && otherBuilding.getType().toLowerCase().equals(INDUSTRIAL))
            buildings.getNotFullyOccupiedBuildings().put(otherBuildingId, otherBuilding);

        for(String resName: initialResValues.keySet())
            resources.getActualResourcesValues().put(resName, initialResValues.get(resName));

        dwellers.setAvailableDwellers(initialAvailableDwellers);
        dwellers.setNeededDwellers(initialNeededDwellers);
        dwellers.setWorkingDwellers(initialWorkingDwellers);

        // when
        buildings.stopProduction(buildingId, resources, dwellers);

        // then
        for(String resName: expectedResValues.keySet())
            assertEquals(resources.getActualResourcesValues().get(resName), expectedResValues.get(resName));

        if(building.getType().toLowerCase().equals(DOMESTIC) && building.isProducing()){
            assertEquals(dwellers.getAvailableDwellers(), initialAvailableDwellers - building.getWorkingDwellers());
            assertEquals(otherBuilding.getWorkingDwellers(), expectedWorkingDwellers);
        }

        for(String resName: expectedResConsumption.keySet())
            assertEquals(resources.getActualResourcesConsumption().get(resName), expectedResConsumption.get(resName));

        for(String resName: expectedResIncomes.keySet())
            assertEquals(resources.getActualResourcesIncomes().get(resName), expectedResIncomes.get(resName));

        for(String resName: expectedResBalance.keySet())
            assertEquals(resources.getResourcesBalance().get(resName), expectedResBalance.get(resName));

        assertFalse(building.isRunning());

        if(building.getType().toLowerCase().equals(DOMESTIC)){
            List<Building> playerDomesticBuildingsList =
                    new ArrayList<>(buildings.getPlayerDomesticBuildings().values());
            assertEquals(building, playerDomesticBuildingsList.get(playerDomesticBuildingsList.size() - 1));
        }
        else{
            assertEquals(dwellers.getNeededDwellers(), initialNeededDwellers - building.getDwellersAmount());
            assertEquals((Integer)dwellers.getWorkingDwellers(), expectedWorkingDwellers);
            assertEquals(building.getWorkingDwellers(), new Integer(0));
            assertTrue(buildings.getNotFullyOccupiedBuildings().isEmpty());
            assertEquals(otherBuilding.getWorkingDwellers(), expectedOtherBuildingWorkingDwellers);
            List<Building> playerIndustrialBuildingsList =
                    new ArrayList<>(buildings.getPlayerIndustrialBuildings().values());
            assertEquals(building, playerIndustrialBuildingsList.get(playerIndustrialBuildingsList.size() - 1));
        }
    }

    private Object[] parametersForResumeProductionInBuildingTest() {
        return $(
                $(ImmutableMap.of("Wood", 15, "Gold", 5), 2, 2, 4, "Field", "FieldId12345", "Field",
                        "FieldId123456", 2, 2, 4, 2, ImmutableMap.of("Wood", 15, "Gold", 2),
                        ImmutableMap.of("Gold", 3), ImmutableMap.of("Grain", 3),
                        ImmutableMap.of("Grain", 3, "Gold", -3), true, false, false, false),
                $(ImmutableMap.of("Wood", 15, "Bread", 3, "Gold", 5), 0, 2, 0, "House",
                        "HouseID12345", "Field", "FieldId123456", 0, 2, 2, 2,
                        ImmutableMap.of("Wood", 15, "Gold", 2, "Bread", 2),
                        ImmutableMap.of("Bread", 1, "Gold", 3),  ImmutableMap.of("Gold", 1, "Grain", 3),
                        ImmutableMap.of("Gold", -2, "Bread", -1, "Grain", 3),
                        true, false, false, true),
                $(ImmutableMap.of("Wood", 15, "Gold", 5), 0, 2, 0, "Field", "FieldId12345",
                        "Field", "FieldId123456", 0, 0, 0, 0, ImmutableMap.of("Wood", 15, "Gold", 5),
                        ImmutableMap.of("Gold", 0), ImmutableMap.of("Grain", 0),
                        ImmutableMap.of("Grain", 0, "Gold", 0), false, false, true, false),
                $(ImmutableMap.of("Wood", 15, "Bread", 0), 0, 2, 0, "House", "HouseID12345",
                        "Field", "FieldId123456", 0, 0, 0, 0, ImmutableMap.of("Wood", 15, "Bread", 0),
                        ImmutableMap.of("Bread", 1),  ImmutableMap.of("Gold", 0),
                        ImmutableMap.of("Gold", 0, "Bread", -1), false, true, false, false),
                $(ImmutableMap.of("Wood", 15, "Gold", 0), 2, 2, 4, "Field", "FieldId12345",
                        "Field", "FieldId123456", 2, 2, 4, 2, ImmutableMap.of("Wood", 15, "Gold", 0),
                        ImmutableMap.of("Gold", 3),  ImmutableMap.of("Grain", 0),
                        ImmutableMap.of("Grain", 0, "Gold", -3), false, true, false, false)
        );
    }

    @Test
    @Parameters(method="parametersForResumeProductionInBuildingTest")
    public void resumeProductionInBuildingTest(Map<String, Integer> initialResValues, int initialWorkingDwellers,
                                               int initialNeededDwellers, int initialAvailableDwellers,
                                               String buildingName, String buildingId,
                                               String otherBuildingName, String otherBuildingId,
                                               Integer otherBuildingWorkingDwellers,
                                               Integer expectedNumOfDwellersWorkingInBuilding, Integer expectedWorkingDwellers,
                                               Integer expectedNumOfDwellersWorkingInOtherBuilding,
                                               Map<String, Integer> expectedResValues, Map<String, Integer> expectedResConsumption,
                                               Map<String, Integer> expectedResIncomes, Map<String, Integer> expectedResBalance,
                                               boolean isBuildingProducing, boolean isBuildingUnprovided,
                                               boolean isBuildingNotFullyOccupied, boolean updateNotFullyOccupiedBuilding){
        // given
        Buildings buildings = new Buildings(dependenciesRepresenter);
        Resources resources = new Resources(dependenciesRepresenter);
        Dwellers  dwellers = new Dwellers(dependenciesRepresenter);

        Building building = createBuilding(buildings, buildingName, buildingId, 0);

        Building otherBuilding = new Building(buildingsMap.get(otherBuildingName));
        otherBuilding.setId(otherBuildingId);
        otherBuilding.setWorkingDwellers(otherBuildingWorkingDwellers);
        buildings.getNotFullyOccupiedBuildings().put(otherBuildingId, otherBuilding);

        dwellers.setAvailableDwellers(initialAvailableDwellers);
        dwellers.setNeededDwellers(initialNeededDwellers);
        dwellers.setWorkingDwellers(initialWorkingDwellers);

        for(String resName: initialResValues.keySet())
            resources.getActualResourcesValues().put(resName, initialResValues.get(resName));

        // when
        buildings.resumeProductionInBuilding(building, resources, dwellers);

        // then
        assertTrue(building.isRunning());

        for(String resName: expectedResValues.keySet())
            assertEquals(resources.getActualResourcesValues().get(resName), expectedResValues.get(resName));

        for(String resName: expectedResConsumption.keySet())
            assertEquals(resources.getActualResourcesConsumption().get(resName), expectedResConsumption.get(resName));

        for(String resName: expectedResIncomes.keySet())
            assertEquals(resources.getActualResourcesIncomes().get(resName), expectedResIncomes.get(resName));

        for(String resName: expectedResBalance.keySet())
            assertEquals(resources.getResourcesBalance().get(resName), expectedResBalance.get(resName));

        if(isBuildingUnprovided)
            assertTrue(buildings.getUnprovidedBuildings().containsKey(buildingId));

        assertEquals(building.getWorkingDwellers(), expectedNumOfDwellersWorkingInBuilding);

        if(building.getType().toLowerCase().equals(DOMESTIC) && building.isProducing())
            assertEquals(dwellers.getAvailableDwellers(), initialAvailableDwellers + building.getWorkingDwellers());

        if(building.getType().toLowerCase().equals(INDUSTRIAL)) {
            assertEquals(dwellers.getNeededDwellers(), initialNeededDwellers + building.getDwellersAmount());
            assertEquals((Integer)dwellers.getWorkingDwellers(), expectedWorkingDwellers);
            if(isBuildingNotFullyOccupied)
                assertTrue(buildings.getNotFullyOccupiedBuildings().containsKey(buildingId));
        }

        assertEquals(building.isProducing(), isBuildingProducing);
        assertEquals(otherBuilding.getWorkingDwellers(), expectedNumOfDwellersWorkingInOtherBuilding);

        if(updateNotFullyOccupiedBuilding) {
            assertFalse(buildings.getNotFullyOccupiedBuildings().containsKey(otherBuildingId));
            assertTrue(buildings.getNotFullyOccupiedBuildings().isEmpty());
        }
        else
            assertTrue(buildings.getNotFullyOccupiedBuildings().containsKey(otherBuildingId));
    }

    /* Helpers */

    public Building createBuilding(Buildings buildings, String buildingName, String buildingId, int workingDwellers){
        Building newBuilding = new Building(buildingsMap.get(buildingName));
        newBuilding.setId(buildingId);
        newBuilding.setWorkingDwellers(workingDwellers);

        if(newBuilding.getType().toLowerCase().equals(DOMESTIC))
            buildings.getPlayerDomesticBuildings().put(buildingId, newBuilding);
        else
            buildings.getPlayerIndustrialBuildings().put(buildingId, newBuilding);

        return newBuilding;
    }
}
