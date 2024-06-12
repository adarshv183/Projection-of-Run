import * as React from "react";
import {
  DiagramComponent,
  Inject,
  DataBinding,
  HierarchicalTree,
} from "@syncfusion/ej2-react-diagrams";
import { DataManager, Query } from "@syncfusion/ej2-data";
//Initializes data source
// const data=[
//     {
//         Id: "parent",
//         Role: "root",
//     },
//     {
//         Id: 1,
//         Role: "1",
//         Team: "parent",
//     },
//     {
//         Id: 7,
//         Role: "7",
//         Team: "1",
//     },
//     {
//         Id: 2,
//         Role: "2",
//         Team: "parent",
//     },
//     {
//         Id: 4,
//         Role: "4",
//         Team: "2",
//     },
//     {
//         Id: 5,
//         Role: "5",
//         Team: "4",
//     },
//     {
//         Id: 6,
//         Role: "6",
//         Team: "4",
//     }
// ];

export default function PolicyTree(policy) {
  const [data, setData] = React.useState([]);

  React.useEffect(() => {
    // Fetch data from the remote link
      fetch("http://127.0.0.1:5000/get_policy_tree", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ data: policy }),
      })
        .then((response) => response.json())
        .then((data) => setData(data))
        .catch((error) => console.error("Error fetching data:", error));
  }, []);
  let items = new DataManager(data, new Query().take(5));
  return (
    <DiagramComponent
      id="container"
      width={"100%"}
      height={"550px"}
      //Uses layout to auto-arrange nodes on the diagram page
      layout={{
        //set the type as Organizational Chart
        type: "OrganizationalChart",
        enableAnimation: true,
        margin: { top: 20 },
        horizontalSpacing: 25,
        verticalSpacing: 30,
        horizontalAlignment: "Left",
        verticalAlignment: "Top",
      }}
      //Configures data source for diagram
      dataSourceSettings={{
        id: "Id",
        parentId: "Team",
        dataManager: items,
      }}
      //Sets the default properties for nodes and connectors
      getNodeDefaults={(obj) => {
        obj.shape = {
          type: "Text",
          content: obj.data.Role,
        };
        obj.style = {
          fill: "None",
          strokeColor: "none",
          strokeWidth: 2,
          bold: true,
          color: "white",
        };
        obj.borderColor = "white";
        obj.backgroundColor = "#6BA5D7";
        obj.borderWidth = 1;
        obj.width = 75;
        obj.height = 40;
        obj.shape.margin = {
          left: 5,
          right: 5,
          top: 5,
          bottom: 5,
        };
        return obj;
      }}
      getConnectorDefaults={(connector, diagram) => {
        connector.style = {
          strokeColor: "#6BA5D7",
          strokeWidth: 2,
        };
        connector.targetDecorator.style.fill = "#6BA5D7";
        connector.targetDecorator.style.strokeColor = "#6BA5D7";
        connector.type = "Orthogonal";
        return connector;
      }}
    >
      <Inject services={[DataBinding, HierarchicalTree]} />
    </DiagramComponent>
  );
}
// const root = ReactDOM.createRoot(document.getElementById("diagram"));
// root.render(<App />);
