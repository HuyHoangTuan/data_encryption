import {Button, Paper, Checkbox, FormControlLabel, TextField, FormControl, Box, styled} from "@mui/material";
import Grid from "@mui/material/Unstable_Grid2"
import React, {useEffect, useState} from "react";
import "./GUI.css"
import APIManager from "../api/APIManager";


const GUI = () => {
    const [audioFile, setAudioFile] = useState(null);
    const [fileName, setFileName] = useState("");
    const Item = styled(Paper)(({theme}) => (
        {
            backgroundColor: theme.palette.mode === 'dark' ? '#1A2027' : '#fff',
            ...theme.typography.body2,
            padding: theme.spacing(1),
            textAlign: 'center',
            color: theme.palette.text.secondary,
        })
    );

    const onProcessRequest = async () => {
        const formData = new FormData();
        formData.append("file", audioFile);

        let headers = {
            "Content-Type": "multipart/form-data",
        }
        let params = {}

        let test = APIManager.post('/api/postRequestTest', headers, params, formData);
        console.log(test);
        test
            .then((res) => {
                console.log(res);
            })
            .catch((err) => {
                console.log(`Err: ${err}`);
            });
    };

    let handleFile = (e) => {

        setAudioFile(e.target.files[0]);
        setFileName(e.target.files[0].name)
    }

    return (
        <>
            <Box sx={{flexGrow: 1, marginTop: "200px"}}>
                <Grid
                    xs={12}
                    container
                    justifyContent="space-around"
                    alignItems="center"
                    flexDirection={{xs: 'column', sm: 'row'}}
                    sx={{fontSize: '12px'}}
                >
                    <Grid sx={{order: {xs: 2, sm: 1, mt: 200}}}>
                        <Item>
                            <form

                            >
                                <input

                                    type="file"
                                    accept="audio/*"
                                    onChange={handleFile}
                                />
                                <span>
                        {fileName}
                      </span>
                            </form>
                        </Item>
                    </Grid>
                    <Grid sx={{order: {xs: 2, sm: 1, mt: 200}}}>
                        <Item>
                            <div id="filterbank-checkbox">
                                <FormControlLabel
                                    control={<Checkbox defaultChecked/>}
                                    label="Enable Filterbank"
                                />
                            </div>
                        </Item>
                    </Grid>
                    <Grid sx={{order: {xs: 2, sm: 1, mt: 200}}}>
                        <Item>
                            <div id="process-button">
                                <Button variant="contained" onClick={onProcessRequest}>
                                    Process
                                </Button>
                            </div>
                        </Item>
                    </Grid>
                </Grid>
                <Grid container spacing={2}
                      sx={{fontSize: '12px', marginTop: "200px"}}
                >
                    <Grid xs={4}>
                        <Item>
                            <div id="song-detail-form">
                                <FormControl fullWidth>
                                    <TextField
                                        disabled
                                        label="Title"
                                        defaultValue=""
                                        variant="filled"
                                    />
                                    <TextField
                                        disabled
                                        label="Length"
                                        defaultValue=""
                                        variant="filled"
                                    />
                                    <TextField
                                        disabled
                                        label="Bit rate"
                                        defaultValue=""
                                        variant="filled"
                                    />
                                    <TextField
                                        disabled
                                        label="Item Type"
                                        defaultValue=""
                                        variant="filled"
                                    />
                                    <TextField
                                        disabled
                                        label="Size"
                                        defaultValue=""
                                        variant="filled"
                                    />
                                </FormControl>
                            </div>
                        </Item>
                    </Grid>
                    <Grid xs={8}>
                        <Item>
                            <div id="result-form">
                                <div></div>
                                <div></div>
                                <Button variant="contained" className="buttonUI">
                                    Download
                                </Button>
                            </div>
                        </Item>
                    </Grid>
                </Grid>
            </Box>
        </>
    );
}

export default GUI;
