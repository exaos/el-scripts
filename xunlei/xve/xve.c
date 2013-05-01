/*
tabsize:4
女孩不哭 23:35 2012-8-18
*/
#include <stdio.h>
#include <string.h>
#define _WIN32_WINNT 0x0502
#include <Windows.h>

int cntFileProcessed = 0;	//count file that processed, accumulated.
int scrWidth;				//screen width

void ResetCursorPos(void)
{
	CONSOLE_SCREEN_BUFFER_INFO sbi;
	COORD co;
	HANDLE hOutput;
	hOutput = GetStdHandle(STD_OUTPUT_HANDLE);
	GetConsoleScreenBufferInfo(hOutput, &sbi);
	co.X = sbi.dwCursorPosition.X-(5+1+4);	//e.g.:1024M,100%
	co.Y = sbi.dwCursorPosition.Y;
	SetConsoleCursorPosition(hOutput, co);
	//sure to leave hOutput as it was
	return;	
}

void ExtractFile(char* filespec)
{
#define BUFSIZE ((1<<20)*5)	//5M buffer
	HANDLE hFileIn = NULL;	//handle of input file
	HANDLE hFileOut = NULL;	//handle of output file

	DWORD dwSizeRead = 0;	//the ReadFile function Read size
	DWORD dwSizeWritten = 0;//the WriteFile function Written size
	DWORD dwSize = 0;
	
	int magicNumber = 0;	//you may know when you look, I suppose.
	int fileType = 0;		//indicates what file it is

	LARGE_INTEGER li;		//for SetFilePointer function use,2M offset of REAL movie data

	BYTE hdr[4];			//the *.xv file header
	BYTE ch;				//
	char* pchar;			//tmp use
	char fileOut[MAX_PATH];	//namely, the output file
	BYTE* buffer = NULL;	//block extraction data, every time it extracts 5MB data at most

	char* errMsg = NULL;	//FormatMessage
	int lastErr = 0;		//GetLastError

	int percent = 0;		//percentage of processed data
	int readSize = 0;		//total size Read
	DWORD fileSize;			//total file size, for percentage use

	int prtLen;				//the printf(and its relative) returned
	int dotLen;				//as you see at the screen

	int k;					//I think you know...
	
	li.LowPart = 1<<21;
	li.HighPart = 0;

	buffer = (BYTE*)malloc(BUFSIZE);	//5M buffer size
	if(buffer == NULL)
	{
		fprintf(stderr, "内存分配失败!\n");
		return;
	}

	hFileIn = CreateFile(filespec, GENERIC_READ, FILE_SHARE_READ, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
	if(hFileIn == INVALID_HANDLE_VALUE)
	{
		free(buffer);
		buffer = NULL;
		lastErr = GetLastError();
		if(FormatMessage(FORMAT_MESSAGE_FROM_SYSTEM|FORMAT_MESSAGE_ALLOCATE_BUFFER, NULL, lastErr, MAKELANGID(LANG_NEUTRAL, SUBLANG_NEUTRAL), (LPSTR)&errMsg, 1, NULL))
		{
			fprintf(stderr, "CreateFile:%s\n%s", filespec, errMsg);
			LocalFree((HLOCAL)errMsg);
			errMsg = NULL;
		}
		return;
	}
	fileSize = GetFileSize(hFileIn, NULL);
	if(fileSize <= 0x00200000)
	{
		fprintf(stderr, "文件大小不正确,不能小于2M.(%s)\n", filespec);
		free(buffer);
		buffer = NULL;
		CloseHandle(hFileIn);
		hFileIn = NULL;
		return;
	}

	fileSize -= 0x00200000;	//2M offset of REAL Video data

	SetFilePointerEx(hFileIn, li, NULL, FILE_BEGIN);
	if(!ReadFile(hFileIn, hdr, 4, &dwSizeRead, NULL) || dwSizeRead==0)
	{
		lastErr = GetLastError();
		if(FormatMessage(FORMAT_MESSAGE_FROM_SYSTEM|FORMAT_MESSAGE_ALLOCATE_BUFFER, NULL, lastErr, MAKELANGID(LANG_NEUTRAL, SUBLANG_NEUTRAL), (LPSTR)&errMsg, 1, NULL))
		{
			fprintf(stderr, "ReadFile:%s\n%s", filespec, errMsg);
			LocalFree((HLOCAL)errMsg);
			errMsg = NULL;
		}
		CloseHandle(hFileIn);
		hFileIn = NULL;
		free(buffer);
		buffer = NULL;
		return;
	}
	
	magicNumber = (338-hdr[1])&0xFF;
	if((BYTE)(hdr[1]+magicNumber)=='R' && (BYTE)(hdr[2]+magicNumber)=='M' && (BYTE)(hdr[3]+magicNumber)=='F')
	{
		fileType = 1;
		goto _go;
	}
	
	magicNumber = (294-hdr[1])&0xFF;
	if((BYTE)(hdr[2]+magicNumber)==178 && (BYTE)(hdr[3]+magicNumber)==117)		
	{
		fileType = 2;
		goto _go;
	}

	magicNumber = (332-hdr[1])&0xFF ;
    if((BYTE)(hdr[1]+magicNumber)==76 && (BYTE)(hdr[2]+magicNumber)==86)
    {
        fileType = 3 ;
        goto _go;
    }

    magicNumber=(329-hdr[1])&0xFF ;
    if((BYTE)(hdr[1]+magicNumber)==73 && (BYTE)(hdr[2]+magicNumber)==70 && (BYTE)(hdr[3]+magicNumber)==70)
    {
        fileType = 4 ;
        goto _go;
    }
    magicNumber=(256-hdr[1])&0xFF ;
    if(!(magicNumber+hdr[2]))
    {
        fileType = 5 ;
        goto _go;
    }

    magicNumber=(256-hdr[1])&0xFF ;
    if((BYTE)(hdr[2]+magicNumber)==1 && (BYTE)(hdr[3]+magicNumber)==186)
    {
        fileType = 6 ;
        goto _go;
    }

    magicNumber=(325-hdr[1])&0xFF ;
    if((BYTE)(hdr[1]+magicNumber)==69 && (BYTE)(hdr[2]+magicNumber)==223 && (BYTE)(hdr[3]+magicNumber)==163)
    {
        fileType = 7 ;
        goto _go;
    }

	fprintf(stderr, "不能识别的文件格式!(%s)\n", filespec);
	free(buffer);
	buffer = NULL;
	CloseHandle(hFileIn);
	hFileIn = NULL;
	return;

_go:
	ch = 0;
	pchar = strrchr(filespec,'\\');
	if(!pchar)
		pchar = strrchr(filespec, '/');
	pchar = pchar==NULL?filespec:pchar+1;
	switch(fileType)
	{
	case 1://rm/rmvb
		ch = 46;
		sprintf(fileOut, "%s%s", pchar, ".rmvb");
		break;
	case 2://wmv
		ch = 48;
		sprintf(fileOut, "%s%s", pchar, ".wmv");
		break;
	case 3://flv
		ch = 70;
		sprintf(fileOut, "%s%s", pchar, ".flv");
		break;
	case 4://avi
		ch = 82;
		sprintf(fileOut, "%s%s", pchar, ".avi");
		break;
	case 5://mp4
		ch = 0;
		sprintf(fileOut, "%s%s", pchar, ".mp4");
		break;
	case 6://mpeg
		ch = 0;
		sprintf(fileOut, "%s%s", pchar, ".mpeg");
		break;
	case 7://mkv
		ch = 26;
		sprintf(fileOut, "%s%s", pchar, ".mkv");
		break;
	default:
		break;
	}
	hFileOut = CreateFile(fileOut, GENERIC_WRITE, FILE_SHARE_READ, NULL, /*CREATE_ALWAYS*/CREATE_NEW, FILE_ATTRIBUTE_NORMAL, NULL);
	if(hFileOut == INVALID_HANDLE_VALUE)
	{
		lastErr = GetLastError();
		if(FormatMessage(FORMAT_MESSAGE_FROM_SYSTEM|FORMAT_MESSAGE_ALLOCATE_BUFFER, NULL, lastErr, MAKELANGID(LANG_NEUTRAL, SUBLANG_NEUTRAL), (LPSTR)&errMsg, 1, NULL))
		{
			fprintf(stderr, "CreateFile:%s\n%s", fileOut, errMsg);
			LocalFree((HLOCAL)errMsg);
			errMsg = NULL;
		}
		CloseHandle(hFileIn);
		hFileIn = NULL;
		free(buffer);
		buffer = NULL;
		return;
	}
	
	WriteFile(hFileOut, (LPVOID)&ch, 1, &dwSizeWritten, NULL);
	
	//handle file header
	for(k = 1; k < 4; k++)
		hdr[k] = (BYTE)((hdr[k]+magicNumber)&0xFF);
	WriteFile(hFileOut, &hdr[1], 3, &dwSizeWritten, NULL);

	//handle encrypted data. is it simple?
	ReadFile(hFileIn, buffer, 1019, &dwSizeRead, NULL);
	for(k=0; k<1019; k++)
		buffer[k] = (BYTE)(buffer[k]+magicNumber & 0xFF);
	WriteFile(hFileOut, buffer, 1019, &dwSizeWritten, NULL);

	readSize += 1024;
	prtLen = printf("%s(%s)", filespec, strrchr(fileOut, '.'));
	dotLen = scrWidth-prtLen%scrWidth;
	if(dotLen<=10)
		dotLen += scrWidth;
	dotLen -= 1;
	while(dotLen--)
		printf(".");
	//it looks like this: left edge-->|mymov.xv(.flv).............1024M, 99% | <--right edge

	//copy rest file, original :-), and show sth. useful. how smart thunder kankan was.
	while(ReadFile(hFileIn, buffer, BUFSIZE, &dwSizeRead, NULL) && dwSizeRead != 0)
	{
		WriteFile(hFileOut, buffer, dwSizeRead, &dwSizeWritten, NULL);
		readSize += dwSizeRead;
		ResetCursorPos();
		printf("%4dM,%3d%%", (int)(readSize/(1<<20)), (int)(readSize/(float)fileSize*100));
	}
	printf("\n");
	CloseHandle(hFileIn);
	CloseHandle(hFileOut);
	hFileIn = NULL;
	hFileOut = NULL;
	free(buffer);
	buffer = NULL;

	cntFileProcessed++;
	return;
}

//parse if there to be a wild char
void HandleFile(char* filespec)
{
	WIN32_FIND_DATA fd;
	HANDLE hFile = NULL;
	char findpath[260];
	char tmppath[260];
	char* pchar = NULL;

	hFile = FindFirstFile(filespec, &fd);
	if(hFile == INVALID_HANDLE_VALUE)
	{
		fprintf(stderr, "没有文件用于处理!\n");
		return;
	}

	strncpy(findpath, filespec, sizeof(findpath));
	//we need to add a full current path to the dest file 
	//since the fd.cFileName member does not include the path
	pchar = strrchr(findpath, '\\');
	if(!pchar)
		pchar = strrchr(findpath, '/');	//sometimes, it's not back-slash-ed.
	if(pchar)
		*(pchar+1) = '\0';
	do 
	{
		if(!(fd.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY))	//eliminate directory
		{
			if(pchar)
			{
				sprintf(tmppath, "%s%s", findpath, fd.cFileName);	//now it's full path
				ExtractFile(tmppath);
			}
			else
			{
				ExtractFile(fd.cFileName);	//in current dir
			}
		}
	} while (FindNextFile(hFile, &fd));	//continue deep search
	FindClose(hFile);
	hFile = NULL;
	return;
}

void Usage(char* name)
{
	char* ptr = strrchr(name, '\\');	//only the name we need, not the full path
	char* pmsg = 
		"迅雷看看XV文件提取器 - 版本:1.0\n"
		"作者:女孩不哭 编译时间:" __DATE__ " " __TIME__ "\n\n"
		"使用方法:\"%s /y 文件\", 输出文件在当前工作目录下\n\n"
		"敬告:迅雷XV文件包含受版权保护的内容.\n"
		"本程序仅供研究和学习使用, 请自觉将提取的文件立即删除.\n"
		"切勿将本程序及其提取的文件使用于任何其它用途.\n"
		"对于使用本程序造成的任何后果, 由使用者自行承担法律责任!\n"
		"要接受此协议, 请从命令行传入/y作为第1个参数, 文件作为第2个参数.\n";
	if(!ptr)
		ptr = strrchr(name, '/');
	if(!ptr)	//the cur dir is just in the exe dir
		ptr = name-1;//ptr+1
	printf(pmsg, ptr+1);
	return;
}

int main(int argc, char** argv)
{
	CONSOLE_SCREEN_BUFFER_INFO sbi;
	if(argc!=3 || stricmp(argv[1], "/y"))	//xve /y file format expected
	{
		Usage(argv[0]);
		return 1;
	}
	GetConsoleScreenBufferInfo(GetStdHandle(STD_OUTPUT_HANDLE), &sbi);
	scrWidth = sbi.dwSize.X;	//width, in characters

	HandleFile(argv[2]);	//enum files if a wild char is detected
	printf("处理了 %d 个文件!\n", cntFileProcessed);
	return 0;
}