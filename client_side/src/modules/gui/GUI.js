import {Button, Paper, Checkbox, FormControlLabel, TextField, FormControl, Box, styled} from "@mui/material";
import Grid from "@mui/material/Unstable_Grid2"
import React, {useState} from "react";
import "./GUI.css"


const GUI = () =>
{
    const [file, setFile] = useState(null);
    const [fileURL, setFileURL] = useState("");

    const Item = styled(Paper)(({ theme }) => ({
      backgroundColor: theme.palette.mode === 'dark' ? '#1A2027' : '#fff',
      ...theme.typography.body2,
      padding: theme.spacing(1),
      textAlign: 'center',
      color: theme.palette.text.secondary,
    }));
    return (
        <>
          <Box sx={{ flexGrow: 1, marginTop: "200px"}}>
            <Grid
              xs={12}
              container
              justifyContent="space-around"
              alignItems="center"
              flexDirection={{ xs: 'column', sm: 'row' }}
              sx={{ fontSize: '12px'}}
            >
              <Grid sx={{ order: { xs: 2, sm: 1, mt: 200} }}>
                <Item>
                  <div id="upload-button">
                    <form>
                      <input type="file" name="file" accept=".wav"/>
                    </form>
                  </div>
                </Item>
              </Grid>
              <Grid sx={{ order: { xs: 2, sm: 1, mt: 200 } }}>
                <Item>
                  <div id="filterbank-checkbox">
                    <FormControlLabel
                      control={<Checkbox defaultChecked />}
                      label="Enable Filterbank"
                    />
                  </div>
                </Item>
              </Grid>
              <Grid sx={{ order: { xs: 2, sm: 1, mt: 200 } }}>
                <Item>
                  <div id="process-button">
                    <Button variant = "contained">
                      Process
                    </Button>
                  </div>
                </Item>
              </Grid>
            </Grid>
            <Grid container spacing={2}
                  sx={{ fontSize: '12px', marginTop: "200px" }}
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
