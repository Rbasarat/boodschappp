import { Grid } from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";
import React, { useContext } from "react";
import { StoresContext } from "../../context/storeContext";
import { Types } from "../../context/storeReducer";
import CheckCircleIcon from "@material-ui/icons/CheckCircle";
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
  checkMark: {
    float: "right",
    position: "relative",
    top: "10px",
    left: "20px",
    color: "green",
  },
  gridItem: {
    margin: "10px",
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

  const storeImages = state.stores.map((store) => (
    <Grid key={store.id} item xs={3} md={1} className={classes.gridItem}>
      <img
        id={store.id}
        src={store.logo}
        alt="Winkel logo"
        className={`${classes.logo}`}
        onClick={() => {
          setStoreIsActive(store.id);
        }}
      />
    </Grid>
  ));

  return (
    <Grid container direction="column" alignItems="center" justify="center">
      <div className={classes.marginBottom}>Selecteer de supermarkten die je wilt vergelijken</div>
      <Grid container direction="row" alignItems="center" justify="center" spacing={2}>
        {state.stores.length > 0 ? (
          storeImages
        ) : (
          <h2>Er zijn op dit moment geen supermarkten beschikbaar. Excuses voor het ongemak.</h2>
        )}
      </Grid>
    </Grid>
  );
};

export default Stores;
