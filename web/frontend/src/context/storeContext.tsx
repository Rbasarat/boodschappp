import React, { createContext, useReducer } from "react";
import { storeReducer, StoreActions } from "./storeReducer";

type StoreType = {
  id: string;
  name: string;
  active: boolean;
};

type InitialStateType = {
  stores: StoreType[];
};
const initialState: InitialStateType = {
  stores: [
    { id: "ah", active: false, name: "ah" },
    { id: "deen", active: false, name: "deen" },
    { id: "dirk", active: false, name: "dirk" },
  ],
};

const StoresContext = createContext<{
  state: InitialStateType;
  dispatch: React.Dispatch<StoreActions>;
}>({
  state: initialState,
  dispatch: () => null,
});

const mainReducer = ({ stores }: InitialStateType, action: StoreActions) => ({
  stores: storeReducer(stores, action),
});

const StoresProvider: React.FC = ({ children }) => {
  const [state, dispatch] = useReducer(mainReducer, initialState);

  return <StoresContext.Provider value={{ state, dispatch }}>{children}</StoresContext.Provider>;
};

export { StoresContext, StoresProvider };
