import React from 'react';
import { SvgIcon, SvgIconProps } from '@material-ui/core';
import { ReactComponent as CactusIcon } from './images/cactus.svg';

export default function Keys(props: SvgIconProps) {
  return <SvgIcon component={CactusIcon} viewBox="0 0 150 58" {...props} />;
}
