type ActionMap<M extends { [index: string]: unknown }> = {
  [Key in keyof M]: M[Key] extends undefined
    ? {
        type: Key;
      }
    : {
        type: Key;
        payload: M[Key];
      };
};

export enum Types {
  setIsSelected = "SET_IS_SELECTED",
}

type StoreType = {
  id: string;
  storeName: string;
  isActive: boolean;
  logo: string;
  isSelected: boolean;
};

type StorePayload = {
  [Types.setIsSelected]: {
    id: string;
  };
};

export type StoreActions = ActionMap<StorePayload>[keyof ActionMap<StorePayload>];

export const storeReducer = (state: StoreType[], action: StoreActions): StoreType[] => {
  switch (action.type) {
    case "SET_IS_SELECTED":
      return state.map((item) => (item.id === action.payload.id ? { ...item, isSelected: !item.isSelected } : item));
    default:
      return state;
  }
};
