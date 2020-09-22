import { makeStyles } from "@material-ui/core/styles";
import { Grid } from "@material-ui/core";
import React, { useContext } from "react";
import { StoresContext } from "../../context/storeContext";
import { Types } from "../../context/storeReducer";
const useStyles = makeStyles(() => ({
  logo: {
    width: "100%",
    height: "100%",
  },

  gridList: {
    flexWrap: "nowrap",
    // Promote the list into his own layer on Chrome. This cost memory but helps keeping high FPS.
    transform: "translateZ(0)",
  },
  marginBottom: {
    marginBottom: "1em",
  },
}));
const Stores: React.FC = () => {
  const classes = useStyles();
  const { state, dispatch } = useContext(StoresContext);

  const setStoreIsActive = (id: string) => {
    dispatch({
      type: Types.setIsActive,
      payload: {
        id: id,
      },
    });
  };
  return (
    <Grid container direction="column" alignItems="center" justify="center">
      <div className={classes.marginBottom}>Selecteer de supermarkten die je wilt vergelijken</div>
      <Grid container direction="row" alignItems="center" justify="center" spacing={2}>
        <Grid item xs={3} md={1}>
          <img
            id="ah"
            src="/icons/ah_logo.svg"
            alt="Boodschappp logo"
            className={classes.logo}
            onClick={() => {
              setStoreIsActive("ah");
            }}
            hidden={
              state.stores.find((ele) => {
                if (ele.id == "ah") return ele;
              })?.active
            }
          />
        </Grid>
        <Grid item xs={3} md={1}>
          <img
            src="/icons/deen_logo.svg"
            alt="Boodschappp logo"
            className={classes.logo}
            onClick={() => {
              setStoreIsActive("ah");
            }}
          />
        </Grid>
        <Grid item xs={3} md={1}>
          <img src="/icons/dirk_logo.svg" alt="Boodschappp logo" className={classes.logo} />
        </Grid>
      </Grid>
    </Grid>
  );
};

export default Stores;
