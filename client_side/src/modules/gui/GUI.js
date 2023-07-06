import {Button, Paper, Checkbox, FormControlLabel, TextField, FormControl, Box, styled} from "@mui/material";
import Grid from "@mui/material/Unstable_Grid2"
import React, {useEffect, useState} from "react";
import "./GUI.css"
import {GUI_STATE} from "../const/const";
import APIManager from "../api/APIManager";


const GUI = () => {
    const [audioFile, setAudioFile] = useState(null);
    const [fileName, setFileName] = useState("");
    let [imageURL, setImageURL] = useState("");
    let [size, setSize] = useState("");
    let [compressRateByBitRate, setCompressRateByBitRate] = useState("");
    let [compressRateByFileSize, setCompressRateByFileSize] = useState("");

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
        
        setImageURL(null);
        APIManager.post('/api/get_plot_image', headers, params, responseType, formData)
            .then((res) => {
                let base64Data = btoa(
                    new Uint8Array(res.data).reduce(
                        (data, byte) => data + String.fromCharCode(byte),
                        ''
                    )
                );
                let _src = `data:image/png;base64,${base64Data}`;
                setImageURL(_src);
            })
            .catch((err) => {
                console.log(`Err: ${err}`)
            })


        setLoadingState(GUI_STATE.LOADING)
        APIManager.post('/api/compress_audio', headers, params, null, formData)
            .then((res) => {
                setCompressRateByBitRate(res.data.compression_rate_by_bit_rate);
                setCompressRateByFileSize(res.data.compression_rate_by_file_size);
                setSize(res.data.file_size);
                setLoadingState(GUI_STATE.DONE);
            })
            .catch((err) => {
                console.log(`Err: ${err}`)
            })
    };

    let handleFile = (e) => {

        setAudioFile(e.target.files[0]);
        setFileName(e.target.files[0].name)
    }

    useEffect(() => {
        switch (loadingState) {
            case GUI_STATE.NOTHING:
                
                break;

            case GUI_STATE.LOADING:
                setSize('Loading...')
                setCompressRateByFileSize('Loading...');
                setCompressRateByBitRate('Loading...');
                break;

            case GUI_STATE.DONE:
                break;
        }
    }, [loadingState])
    return (
        <>
            <Box sx={{flexGrow: 1, marginTop: "50px"}}>
                <Grid
                    container
                    justifyContent="space-around"
                    alignItems="center"
                    flexDirection={{xs: 'column', sm: 'row'}}
                    sx={{fontSize: '12px'}}
                >
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
                    <Item>
                        <div id="filterbank-checkbox">
                            <FormControlLabel
                                control={<Checkbox defaultChecked/>}
                                label="Enable Filterbank"
                            />
                        </div>
                    </Item>
                    <Item>
                        <div id="process-button">
                            <Button variant="contained" onClick={onProcessRequest}>
                                Process
                            </Button>
                        </div>
                    </Item>
                </Grid>
                <Grid
                    container
                    spacing={4}
                    justifyContent="center"
                    sx={{fontSize: '12px', marginTop: "50px"}}
                >
                    <Item
                        style={
                            {
                                width: '400px',
                                height: '450px'
                            }
                        }
                    >
                        <div id="song-detail-form"
                             style={
                                 {
                                     position: 'absolute',
                                     width: '400px',
                                     height: '450px',
                                 }
                             }
                        >
                            <FormControl
                                fullWidth
                                style={
                                    {
                                        position: 'absolute',
                                        left: '50%',
                                        top: '50%',
                                        transform: 'translate(-50%, -50%)'
                                    }
                                }
                            >
                                <TextField
                                    disabled
                                    label="Old/New Size"
                                    value={compressRateByFileSize}
                                    variant="filled"
                                />
                                <TextField
                                    disabled
                                    label="Compression Rate By File Size"
                                    value={compressRateByFileSize}
                                    variant="filled"
                                />
                                <TextField
                                    disabled
                                    label="Compression Rate By Bit Rate"
                                    value={compressRateByBitRate}
                                    variant="filled"
                                />
                            </FormControl>
                        </div>
                    </Item>
                    <Item
                        style={
                            {
                                width: '800px',
                                height: '450px'
                            }
                        }
                    >
                        <div
                            id="result-form"
                            style={
                                {
                                    position: 'absolute',
                                    width: '800px',
                                    height: '450px'
                                }
                            }
                        >
                            <div className="image-container">
                                <Paper elevation={2} style={{width: '100%', height: '100%'}}>
                                    {
                                        imageURL && <img
                                            src={imageURL}
                                            style={
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
                                    {
                                        !imageURL && loadingState == GUI_STATE.LOADING && <span
                                            style={
                                                {
                                                    fontSize: '20px',
                                                    left: '50%',
                                                    top: '50%',
                                                    position: 'absolute',
                                                    transform: 'translate(-50%, -50%)'
                                                }
                                            }
                                        >
                                            Loading...
                                        </span>
                                    }
                                </Paper>
                            </div>
                            <div
                                style={
                                    {
                                        position: "absolute",
                                        bottom: "0%",
                                        left: "50%",
                                        transform: 'translateX(-50%)'
                                    }
                                }
                            >
                                <Button variant="contained" className="buttonUI">
                                    Download
                                </Button>
                            </div>
                        </div>
                    </Item>
                </Grid>
            </Box>
        </>
    );
}

export default GUI;
