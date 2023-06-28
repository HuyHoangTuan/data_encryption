import React from "react";
import {RouterProvider} from "react-router-dom";
import CustomRouter from "./router/Router";

function App()
{
    return(
        <React.Fragment>
            <RouterProvider router={CustomRouter}/>
        </React.Fragment>
    )
}

export default App;