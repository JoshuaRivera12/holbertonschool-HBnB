digraph HBnB_Architecture {
    rankdir=TB;
    
    subgraph cluster_PresentationLayer {
        label="Presentation Layer";
        style=filled;
        color=lightblue;
        API [label="Service API", shape=box, style=filled, fillcolor=white];
    }
    
    subgraph cluster_BusinessLogicLayer {
        label="Business Logic Layer";
        style=filled;
        color=lightgreen;
        Models [label="Model Classes (User, Place, Review, Amenity)", shape=box, style=filled, fillcolor=white];
    }
    
    subgraph cluster_PersistenceLayer {
        label="Persistence Layer";
        style=filled;
        color=lightcoral;
        Database [label="Database Access", shape=box, style=filled, fillcolor=white];
    }
    
    API -> Models [label="Facade Pattern"];
    Models -> Database [label="Database Operations"];
}

