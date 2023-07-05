import {Button, Paper, Checkbox, FormControlLabel, TextField, FormControl, Box, styled} from "@mui/material";
import Grid from "@mui/material/Unstable_Grid2"
import React, {useEffect, useState} from "react";
import "./GUI.css"
import { GUI_STATE } from "../const/const";
import APIManager from "../api/APIManager";


const GUI = () => {
    const [audioFile, setAudioFile] = useState(null);
    const [fileName, setFileName] = useState("");
    let [imageURL, setImageURL] = useState("");
    let [compressRate, setCompressRate] = useState("");
    let [loadingState, setLoadingState] = useState(GUI_STATE.DONE);
    let [data, setData] = useState(
        {
            title: '',
            length: '',
            bit_rate: '',
            item_type: '',
            size: '',
            compression_rate: ''
        }
    )
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
        let responseType = 'arraybuffer'

        APIManager.post('/api/compress_audio', headers, params, responseType, formData)
        .then((res) => {
            handleCompressAudioResponse(res.data);
        })
        .catch((err) =>{
            console.log(`Err: ${err}`)
        })


        setLoadingState(GUI_STATE.LOADING)
        APIManager.post('/api/get_data_audio', headers, params, null, formData)
        .then((res) => {
            handleDataAudioResponse(res.data);
            setLoadingState(GUI_STATE.DONE);
            console.log(res.data);
        })
        .catch((err) =>{
            console.log(`Err: ${err}`)
        })
    };

    let handleCompressAudioResponse = (response) => {
        let base64Data = btoa(
            new Uint8Array(response).reduce(
                (data, byte) => data + String.fromCharCode(byte),
                ''
            )
        );
        let _src = `data:image/png;base64,${base64Data}`;
        setImageURL(_src);
        
    }

    let handleDataAudioResponse = (response) => {
        let comRate = response.compression_rate;
        setCompressRate(comRate);
    }

    useEffect(() => {
        console.log(`Comress: ${compressRate}`);
    }, [compressRate]);

    let handleFile = (e) => {

        setAudioFile(e.target.files[0]);
        setFileName(e.target.files[0].name)
    }

    useEffect(() => {
        switch(loadingState)
        {
            case GUI_STATE.NOTHING:
                break;

            case GUI_STATE.LOADING:
                setCompressRate('Loading...');
                break;

            case GUI_STATE.DONE:
                break;
        }
    }, [loadingState])
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
                                    <TextField
                                        disabled
                                        label="Compression Rate"
                                        value={compressRate}
                                        variant="filled"
                                    />
                                </FormControl>
                            </div>
                        </Item>
                    </Grid>
                    <Grid xs={8}>
                        <Item>
                            <div id="result-form">
                                <div className="image-container">
                                    <Paper elevation={2}>
                                        {
                                            imageURL && <img
                                                src={imageURL}
                                                style = {
                                                    {
                                                        width: "100%",
                                                        height: "100%",
                                                        objectFit: "contain",
                                                        marginLeft: "auto",
                                                        marginRight: "auto"
                                                    }
                                                }
                                            />
                                        }
                                    </Paper>
                                </div>
                                <div className="image-container">
                                    <Paper elevation={2}>
                                    
                                    </Paper>
                                </div>
                                <div className="button-container">
                                    <Button variant="contained" className="buttonUI">
                                        Download
                                    </Button>
                                </div>
                            </div>
                        </Item>
                    </Grid>
                </Grid>
            </Box>
        </>
    );
}

export default GUI;
