import React from "react";
import {Route, createBrowserRouter, createRoutesFromElements} from 'react-router-dom';
import PublicRoute from "./PublicRoute";
import GUI from "../gui/GUI";
import "../gui/GUI.css";

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
                            <GUI/>
                        </React.Fragment>
                    </PublicRoute>
                }
            />
        ]
    )
);

export default CustomRouter;