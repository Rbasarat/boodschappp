import React, { createContext, useReducer, ReactNode } from "react";
import { storeReducer, StoreActions } from "./storeReducer";

type StoreType = {
  id: string;
  storeName: string;
  isActive: boolean;
  logo: string;
  isSelected: boolean;
};

export type InitialStateType = {
  stores: StoreType[];
};

const StoresContext = createContext<{
  state: InitialStateType;
  dispatch: React.Dispatch<StoreActions>;
}>({
  state: { stores: [] },
  dispatch: () => null,
});

const mainReducer = ({ stores }: InitialStateType, action: StoreActions) => ({
  stores: storeReducer(stores, action),
});

interface Props {
  children: ReactNode;
  initialState: InitialStateType;
}

const StoresProvider: React.FC<Props> = ({ children, initialState }: Props) => {
  const [state, dispatch] = useReducer(mainReducer, initialState);

  return <StoresContext.Provider value={{ state, dispatch }}>{children}</StoresContext.Provider>;
};

export { StoresContext, StoresProvider };
