package creatornode;

import constants.Consts;
import controlnode.DispatchCenter;
import entities.Building;
import entities.Dweller;
import entities.Resource;
import graph.*;
import model.DependenciesRepresenter;
import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mock;

import java.util.HashMap;
import java.util.List;

import static org.junit.Assert.*;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

public class GraphsHolderTest {

    @Mock
    private DispatchCenter dispatchCenter;
    private GraphsHolder graphsHolder;

    @Before
    public void setUp() throws Exception {
        dispatchCenter = mock(DispatchCenter.class);
        HashMap<String, DependenciesRepresenter> reprensenters = new HashMap<>();
        when(dispatchCenter.getDispatchData(Consts.LOADER_MODULE, Consts.DEPENDENCIES_REPRESENTERS)).thenReturn(reprensenters);
        new CreatorPy4JNode(dispatchCenter, "Creator",
                "..\\..\\resources\\sysFiles\\defaultDependencies\\");
        DependenciesRepresenter dr = reprensenters.get("Moon");
        assertNotNull(dr);
        graphsHolder = dr.getGraphsHolder();
    }

    @Test
    public void testDwellersDisplayGraph(){
        JSONArray dwellersDispGraph = graphsHolder.displayAllGraphs().getJSONArray(Consts.DWELLERS);
        System.out.println(dwellersDispGraph.toString(4));


        assertEquals(
                "Robotnik",
                dwellersDispGraph
                        .getJSONObject(0)
                        .getString("Name")
        );
        assertEquals(
                "Inwestor",
                dwellersDispGraph
                        .getJSONObject(0)
                        .getJSONArray("Children")
                        .getJSONObject(0)
                        .getString("Name")
        );

        assertEquals(
                "Naukowiec",
                dwellersDispGraph
                        .getJSONObject(0)
                        .getJSONArray("Children")
                        .getJSONObject(0)
                        .getJSONArray("Children")
                        .getJSONObject(0)
                        .getString("Name")
        );
        assertEquals(
                "Xenogenetyk",
                dwellersDispGraph
                        .getJSONObject(0)
                        .getJSONArray("Children")
                        .getJSONObject(0)
                        .getJSONArray("Children")
                        .getJSONObject(0)
                        .getJSONArray("Children")
                        .getJSONObject(0)
                        .getString("Name")
        );
    }

    @Test
    public void testRandomEntityNotNull(){
        for(int i = 0; i < 100; i++) {
            assertNotNull(graphsHolder.getRandomBuilding());
            assertNotNull(graphsHolder.getRandomDweller());
            assertNotNull(graphsHolder.getRandomResource());
        }
    }


    private JSONObject fetchEntityByName(JSONArray entities, String entityName){
        for(int i = 0; i < entities.length(); i++){
            JSONObject potentialHit = entities.getJSONObject(i);
            if (potentialHit.getString("Name").equals(entityName)){
                return potentialHit;
            }
        }
        return null;
    }

    @Test
    public void testBuildingsDisplayGraph(){
        JSONArray buildingsDispGraph = graphsHolder.displayAllGraphs().getJSONArray(Consts.BUILDINGS);
        System.out.println(buildingsDispGraph.toString(4));

        assertNotNull(fetchEntityByName(buildingsDispGraph, "Zrodlo gizmo"));
        assertNotNull(
            fetchEntityByName(
                fetchEntityByName(
                        fetchEntityByName(
                                fetchEntityByName(
                                        buildingsDispGraph,
                                        "Plantacja owocow"
                                ).getJSONArray("Children"),
                                "Wytwornia witamin"
                        ).getJSONArray("Children"),
                        "Browar"
                ).getJSONArray("Children"),
                "Cukiernia"
            )
        );

        assertNotNull(fetchEntityByName(buildingsDispGraph, "Kopalnia gleju"));
        assertNotNull(fetchEntityByName(buildingsDispGraph, "Dormitorium robotnikow"));
        assertNotNull(fetchEntityByName(buildingsDispGraph, "Wytwornia egzoszkieletow"));
        assertNotNull(fetchEntityByName(buildingsDispGraph, "Fabryka energodropsow"));

    }

    @Test
    public void testResourcesDisplayGraph(){
        JSONArray resourcesDispGraph = graphsHolder.displayAllGraphs().getJSONArray(Consts.RESOURCES);
        System.out.println(resourcesDispGraph.toString(4));
        assertNotNull(fetchEntityByName(resourcesDispGraph, "Gizmo"));
        assertNotNull(fetchEntityByName(resourcesDispGraph, "Plastyczny egzoszkielet"));
        assertNotNull(
                fetchEntityByName(
                        fetchEntityByName(
                                fetchEntityByName(
                                        fetchEntityByName(
                                                resourcesDispGraph,
                                                "Owoce"
                                        ).getJSONArray("Children"),
                                        "Witaminy"
                                ).getJSONArray("Children"),
                                "Zdrowy likier"
                        ).getJSONArray("Children"),
                        "Alkoholowe desery"
                )
        );
    }

    private <E extends GraphNode> E fetchEntityNode(List<E> roots, String name){
        for(E root: roots){
            if (root.getName().equals(name)){
                return root;
            }
        }
        return null;

    }

    private BuildingNode fetchBuildingRoot(String name){
        return fetchEntityNode( graphsHolder.getBuildingsGraphs(), name);
    }

    private ResourceNode fetchResourceRoot(String name){
        return fetchEntityNode( graphsHolder.getResourcesGraphs(), name);

    }

    private DwellerNode fetchDwellerRoot(String name){
        return fetchEntityNode(graphsHolder.getDwellersGraphs(), name);
    }

    private Resource getResourceChild(GraphNode node, String name){
        return ((ResourceNode)node.getChild(name)).getResource();
    }

    @Test
    public void testResourcesGraph(){
        ResourceNode fruitsNode = fetchResourceRoot("Owoce");
        assertNotNull(fruitsNode);
        assertEquals("Owoce", fruitsNode.getResource().getName());
        assertEquals(fruitsNode, graphsHolder.getResourceNode("Owoce"));

        ResourceNode vitaminsNode = graphsHolder.getResourceNode("Witaminy");
        Resource vitamins = getResourceChild(fruitsNode, "Witaminy");
        assertNotNull(vitamins);
        assertEquals("Witaminy", vitamins.getName());
        assertEquals(vitaminsNode.getResource(), getResourceChild(fruitsNode, "Witaminy"));

        ResourceNode vodkaNode = graphsHolder.getResourceNode("Zdrowy likier");
        Resource vodka = getResourceChild(vitaminsNode, "Zdrowy likier");
        assertNotNull(vodka);
        assertEquals("Zdrowy likier", vodka.getName());
        assertEquals(vodkaNode.getResource(), getResourceChild(vitaminsNode, "Zdrowy likier"));

        ResourceNode alcoholDesertsNode = graphsHolder.getResourceNode("Alkoholowe desery");
        Resource alcoholDeserts = getResourceChild(vodkaNode, "Alkoholowe desery");
        assertNotNull(alcoholDeserts);
        assertEquals("Alkoholowe desery", alcoholDeserts.getName());
        assertEquals(alcoholDesertsNode.getResource(), getResourceChild(vodkaNode, "Alkoholowe desery"));

        assertNotNull(fetchResourceRoot("Gizmo"));
        assertNotNull(fetchResourceRoot("Plastyczny egzoszkielet"));
    }


    private Building getBuildingChild(GraphNode node, String name){
        return ((BuildingNode)node.getChild(name)).getBuilding();
    }

    @Test
    public void testBuildingsGraph(){
        BuildingNode plantationNode = fetchBuildingRoot("Plantacja owocow");
        assertNotNull(plantationNode);
        assertEquals(plantationNode, graphsHolder.getBuildingNode("Plantacja owocow"));

        BuildingNode workersDormitoryNode = fetchBuildingRoot("Dormitorium robotnikow");
        assertNotNull(workersDormitoryNode);
        assertEquals("Dormitorium robotnikow", workersDormitoryNode.getBuilding().getName());

        BuildingNode investorDormitoryNode = graphsHolder.getBuildingNode("Kompleks inwestorow");
        Building investorDormitory =  getBuildingChild(workersDormitoryNode, "Kompleks inwestorow");
        assertNotNull(investorDormitory);
        assertEquals("Kompleks inwestorow",investorDormitory.getName());
        assertEquals(investorDormitoryNode.getBuilding(), getBuildingChild(workersDormitoryNode, "Kompleks inwestorow"));

        BuildingNode scientistDormitoryNode = graphsHolder.getBuildingNode("Kwatery naukowcow");
        Building scientistDormitory = getBuildingChild(investorDormitoryNode, "Kwatery naukowcow");
        assertNotNull(scientistDormitory);
        assertEquals("Kwatery naukowcow", scientistDormitory.getName());
        assertEquals(scientistDormitoryNode.getBuilding(), getBuildingChild(investorDormitoryNode, "Kwatery naukowcow"));

        BuildingNode xenogenesisPalaceNode = graphsHolder.getBuildingNode("Palac Xenogenetyka");
        Building xenogenesisPalace = getBuildingChild(scientistDormitoryNode, "Palac Xenogenetyka");
        assertNotNull(xenogenesisPalace);
        assertEquals("Palac Xenogenetyka", xenogenesisPalace.getName());
        assertEquals(xenogenesisPalaceNode.getBuilding(), getBuildingChild(scientistDormitoryNode, "Palac Xenogenetyka"));

        BuildingNode energyFactory = fetchBuildingRoot("Fabryka energodropsow");
        assertNotNull(energyFactory);

        assertNotNull(fetchBuildingRoot("Wytwornia egzoszkieletow"));
    }

    private Dweller getDwellerChild(GraphNode node, String name){
        return ((DwellerNode)node.getChild(name)).getDweller();
    }

    @Test
    public void testDwellersGraph(){
        DwellerNode workerNode = fetchDwellerRoot("Robotnik");
        assertNotNull(workerNode);
        assertEquals(workerNode,  graphsHolder.getDwellerNode("Robotnik"));
        assertEquals("Robotnik", workerNode.getDweller().getName());

        DwellerNode investorNode = graphsHolder.getDwellerNode("Inwestor");
        Dweller investor =  getDwellerChild(workerNode, "Inwestor");
        assertNotNull(investor);
        assertEquals("Inwestor",investor.getName());
        assertEquals(investorNode.getDweller(), getDwellerChild(workerNode, "Inwestor"));

        DwellerNode scientistNode = graphsHolder.getDwellerNode("Naukowiec");
        Dweller scientist =  getDwellerChild(investorNode, "Naukowiec");
        assertNotNull(scientist);
        assertEquals("Naukowiec", scientist.getName());
        assertEquals(scientistNode.getDweller(), getDwellerChild(investorNode, "Naukowiec"));

        DwellerNode xenogenesisNode = graphsHolder.getDwellerNode("Xenogenetyk");
        Dweller xenogenesis =  getDwellerChild(scientistNode, "Xenogenetyk");
        assertNotNull(xenogenesis);
        assertEquals("Xenogenetyk", xenogenesis.getName());
        assertEquals(xenogenesisNode.getDweller(), getDwellerChild(scientistNode, "Xenogenetyk"));
    }

}