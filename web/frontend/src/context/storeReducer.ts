type ActionMap<M extends { [index: string]: any }> = {
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
  setIsActive = "SET_IS_ACTIVE",
}

type StoreType = {
  id: string;
  name: string;
  active: boolean;
};

type StorePayload = {
  [Types.setIsActive]: {
    id: string;
  };
};

export type StoreActions = ActionMap<StorePayload>[keyof ActionMap<StorePayload>];

export const storeReducer = (state: StoreType[], action: StoreActions) => {
  switch (action.type) {
    case "SET_IS_ACTIVE":
      return state.map((item) => (item.id === action.payload.id ? { ...item, active: !item.active } : item));
    default:
      return state;
  }
};
