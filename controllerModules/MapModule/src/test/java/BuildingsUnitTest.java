import entities.Building;
import junitparams.JUnitParamsRunner;
import junitparams.Parameters;
import mapnode.Buildings;
import model.DependenciesRepresenter;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;

import java.util.*;

import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

@RunWith(JUnitParamsRunner.class)
public class BuildingsUnitTest {
    private static final String DOMESTIC = "domestic";
    private static final String INDUSTRIAL = "industrial";

    @Mock
    private static DependenciesRepresenter dependenciesRepresenter;

    private static Map<String, Building> buildingsMap;
    private static Map<String, Integer> resourcesMap = new HashMap<>();

    @BeforeClass
    public static void initializeClass(){
        resourcesMap.put("Grain", 0);
        resourcesMap.put("Wood", 0);
        resourcesMap.put("Gold", 0);
        resourcesMap.put("Bread", 0);
        resourcesMap.put("Flour", 0);
    }

    @Before
    public  void initializeTest(){
        dependenciesRepresenter = mock(DependenciesRepresenter.class);

        buildingsMap = new HashMap<>();

        Map<String, Integer> fieldProduces = new HashMap<>(resourcesMap);
        fieldProduces.put("Grain", 3);
        Map<String, Integer> fieldConsumes = new HashMap<>(resourcesMap);
        fieldConsumes.put("Wood", 3);
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
    }

    @Test
    @Parameters({"Field, Wood, 15, true",
                 "Field, Wood, 10, true",
                 "Field, Wood, 7, false",
                 "House, Wood, 15, true",
                 "House, Wood, 14, false"})
    public void testCanAffordOnBuilding(String buildingName, String resourceName, Integer resourceAmount,
                                        boolean expectedResult){
        // given
        Map<String, Integer> actualResValues = new HashMap<>(resourcesMap);
        actualResValues.put(resourceName, resourceAmount);
        Buildings buildings = new Buildings(dependenciesRepresenter);

        // when
        Boolean canAfford = buildings.canAffordOnBuilding(buildingName, actualResValues);

        // then
        assertEquals(canAfford, expectedResult);
    }


    @Test
    @Parameters({"Field, FieldId12345, true",
                 "House, HouseId12345, true",
                 "Field, FieldId12345, false"})
    public void findBuildingWithIdTest(String buildingName, String buildingId, boolean isBuildingIdPresent){
        // given
        Buildings buildings = new Buildings(dependenciesRepresenter);
        String buildingType = buildingsMap.get(buildingName).getType().toLowerCase();
        Building building = new Building(buildingsMap.get(buildingName));

        if(buildingType.equals(DOMESTIC) && isBuildingIdPresent)
            buildings.getPlayerDomesticBuildings().put(buildingId, building);
        if(buildingType.equals(INDUSTRIAL) && isBuildingIdPresent)
            buildings.getPlayerIndustrialBuildings().put(buildingId, building);

        // when
        Building foundBuilding = buildings.findBuildingWithId(buildingId);

        // then
        if(isBuildingIdPresent)
            assertEquals(foundBuilding, building);
        else
            assertEquals(foundBuilding, null);
    }


    @Test
    @Parameters({"Field, true",
                 "House, true",
                 "Castle, false"})
    public void findBuildingWithNameTest(String buildingName, boolean isBuildingWithNamePresent){
        // given
        Buildings buildings = new Buildings(dependenciesRepresenter);

        // when
        Building foundBuilding = buildings.findBuildingWithName(buildingName);

        // then
        if(isBuildingWithNamePresent)
            assertEquals(foundBuilding.getName(), buildingName);
        else
            assertEquals(foundBuilding, null);
    }


    @Test
    @Parameters({"Field, Mill",
                 "House, "})
    public void unlockSuccessorsTest(String buildingName, String unlockedSuccessor){
        // given
        Buildings buildings = new Buildings(dependenciesRepresenter);

        // when
        List<String> unlockedBuildings  = buildings.unlockSuccessors(buildingsMap.get(buildingName));

        // then
        if(!unlockedSuccessor.isEmpty())
            assertTrue(unlockedBuildings.contains(unlockedSuccessor));
        else
            assertTrue(unlockedBuildings.isEmpty());
    }


    @Test
    @Parameters({"Field, FieldId12345, 2, true",
                 "House, HouseId12345, 2, true",
                 "Field, FieldId12345, 1, true",
                 "House, HouseId123456, 1, false"})
    public void getWorkingDwellersTest(String buildingName, String buildingId, Integer workingDwellers,
                                       boolean isBuildingPresent){
        // given
        AssertionError exception = null;
        Buildings buildings = new Buildings(dependenciesRepresenter);
        String buildingType = buildingsMap.get(buildingName).getType().toLowerCase();
        Building building = new Building(buildingsMap.get(buildingName));
        building.setId(buildingId);
        building.setWorkingDwellers(workingDwellers);

        if(buildingType.equals(DOMESTIC) && isBuildingPresent)
            buildings.getPlayerDomesticBuildings().put(buildingId, building);
        if(buildingType.equals(INDUSTRIAL) && isBuildingPresent)
            buildings.getPlayerIndustrialBuildings().put(buildingId, building);

        // when
        Integer actualWorkingDwellers = 0;

        try {
             actualWorkingDwellers = buildings.getWorkingDwellers(buildingId);
        } catch (AssertionError e){
            exception = e;
        }

        // then
        if(isBuildingPresent)
            assertEquals(actualWorkingDwellers, workingDwellers);
        else
            assertNotNull(exception);
    }

}
