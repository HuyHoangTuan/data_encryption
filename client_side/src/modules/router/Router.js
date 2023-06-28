import React from "react";
import {Route, createBrowserRouter, createRoutesFromElements} from 'react-router-dom';
import PublicRoute from "./PublicRoute";

const CustomRouter = createBrowserRouter(
    createRoutesFromElements(
        [
            <Route
                path ="/*"
                loader = {
                    async (props) => {
                        console.log("App loader: "+JSON.stringify(props));
                        return props;
                    }
                }
                element = {
                    <PublicRoute>
                        <React.Fragment>
                            <h1>
                                Erase me then add GUI here
                            </h1>
                        </React.Fragment>
                    </PublicRoute>
                }
            />
        ]
    )
);

export default CustomRouter;